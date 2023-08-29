import base64
import typing
from datetime import datetime

import iso8601
import mailchimp_transactional as MailchimpTransactional
from bson import ObjectId
from mailchimp_transactional.api_client import ApiClientError

from .dates import today_argentina
from .format import muvi_print
from .init_creds import init_mongo, mailchimp_key, test

mailchimp = MailchimpTransactional.Client(mailchimp_key)

def send_mail_with_attachment(
    files_attachments: list,
    receiver_mail,
    test_mail="matias@muvinai.com",
    global_vars:list=list(),
    template: str = 'facturacion',
    brand: dict = {}
):
    print("Enviando mail facturacion...")
    attachment = []
    try:
        for file in files_attachments:
            with open(file['path'], 'rb') as f:
                file_str = f.read()
                file_str = base64.b64encode(file_str)
                file_str = file_str.decode('utf-8')
            muvi_print('info', 'Archivo adjunto procesado con exito')
            attachment.append({
                'content': file_str,
                'name': file['name'].split('/')[-1],
                'type': file['type'] if 'type' in file else 'application/pdf'
            })
    except:
        return 'error: el archivo no pudo ser encontrado o procesado'
    
    if test:
        to_mail = [{"email": test_mail}]
    else:
        to_mail = [{"email": receiver_mail}]
    
    msg = {
        'from_email': brand.get('mail_sender_address'),
        'from_name': brand.get('name'),
        'to': to_mail,
        'global_merge_vars': global_vars,
        'attachments': attachment
    }
    try:
        response = mailchimp.messages.send_template({
            'template_name': template,
            'template_content': [],
            'message': msg
        })
        print(response)
        return response[0]
    except ApiClientError as error:
        print('An exception occurred: {}'.format(error.text))
        return 'error'


def send_mail_to_template(receiver: dict, template: str, brand: dict, plan_name: str = "None") -> dict:
    """ Enviar mail con un template determinado

    :param receiver: objeto de cliente del destinatario
    :type receiver: dict
    :param template: nombre del template
    :type template: str
    :param plan: nombre del plan, defaults to "None"
    :type plan: str, optional
    :return: informacion del mail
    :rtype: dict
    """
    try:
        sdate = receiver["last_subscription_date"].strftime("%d/%m/%Y")

    except AttributeError:
        sdate = iso8601.parse_date(receiver["last_subscription_date"]).strftime("%d/%m/%Y")
    except:
        return {}

    global_vars = [{"name": "nombre", "content": receiver["nombre"]},
                   {"name": "apellido", "content": receiver["apellido"]},
                   {"name": "documento", "content": receiver["documento"]},
                   {"name": "plan", "content": plan_name},
                   {"name": "fecha_subscripcion", "content": sdate}
                   ]
    if brand["name"].lower() != "sportclub":
        global_vars.extend([
            {"name": "logo", "content": brand['images']['mail_logo']},
            {"name": "brand_name", "content": brand["name"]}
        ])
    send_mail(receiver["email"], global_vars, template, brand)


def send_alert(reciever_mail: str, proceso: str, mensaje: str, referencia: str, test_mail="matias@muvinai.com") -> typing.Union[dict, None]:
    """ Enviar mensaje de alerta a ignacio@muvinai.com
    :param reciever_mail: email de quien recibe la alerta
    :type reciever_mail: str
    :param proceso: nombre del proceso
    :type proceso: str
    :param mensaje: mensaje
    :type mensaje: str
    :param referencia: referencia
    :type referencia: str
    :return: Respuesta de mailchimp o None en caso de error
    :rtype: dict | None
    """

    global_vars = [{"name": "proceso", "content": proceso},
                   {"name": "mensaje", "content": mensaje},
                   {"name": "referencia", "content": referencia}
                   ]
    brand = {"mail_sender_address": "no-responder@sportclub.com.ar",
            "name": "SportClub"}
    return send_mail(reciever_mail, global_vars, "alertas", brand, test_mail)


def send_mail_inactivo(
    receiver: dict,
    brand: dict,
    test_mail='matias@muvinai.com'
):
    """ Enviar mail indicando al cliente que está inactivo.

    :param receiver: documento de cliente del destinatario
    :type receiver: dict
    :return: informacion del mail
    :rtype: dict
    """

    db = init_mongo()
    template = 'inactivo'
    global_vars = [{'name': 'nombre', 'content': receiver['nombre']}]

    if brand["name"].lower() != "sportclub":
        template = "inactivo-nosc"
        global_vars.extend([
            {"name": "logo", "content": brand["images"]["mail_logo"]},
            {"name": "brand_name", "content": brand["name"]},
            {"name": "email_contacto", "content": brand["email_contacto"]}
        ])
        return send_mail(receiver["email"], global_vars, template, brand, test_mail)

    merchant_centrales = [doc['_id'] for doc in db.merchants.find({'negocio_central': True}, {'_id': 1})]
    merchant_centrales.append(ObjectId('6178652dcfb117ad58a2cd3d'))

    if receiver.get('status') == 'baja':
        if receiver.get('plan_corporativo', None):
            template = 'inactivacion-por-baja-corpo'
            global_vars.append({'name': 'email_contacto', 'content': 'atencion.socios@sportclub.com.ar'})
        elif receiver.get('merchant_id') in merchant_centrales and not receiver.get('seller_merchant_id', None):
            template = 'inactivacion-por-baja-corpo-cadena'
            global_vars.extend([
                {'name': 'checkout_link', 'content': 'https://www.sportclub.com.ar'},
                {'name': 'email_contacto', 'content': 'atencion.socios@sportclub.com.ar'}
            ])
        else:
            template = 'inactivacion-por-baja-sede'
            email_sede = 'atencion.socios@sportclub.com.ar'
            if (merchant := receiver.get('seller_merchant_id', None)) or (merchant := receiver.get('merchant_id', None)):
                merchant = db.merchants.find_one({'_id': merchant})
                sede = db.club.find_one({'_id': merchant.get('sede_principal')})
                email_sede = sede.get('contact-email')
            
            global_vars.extend([{'name': 'email_contacto', 'content': email_sede}])
    
    if receiver.get('status') == 'activo':
        if receiver.get('merchant_id') in merchant_centrales and not receiver.get('seller_merchant_id', None):
            template = 'inactivaci-n-autom-tica-cadena-corpo'
            global_vars.extend([
                {'name': 'checkout_link', 'content': f"https://www.sportclub.pagar.club/paso2/{receiver.get('slug')}"},
                {'name': 'email_contacto', 'content': 'atencion.socios@sportclub.com.ar'}
            ])
        else:
            template = 'inactivacion-automatica-sede'
            email_sede = 'atencion.socios@sportclub.com.ar'
            if (merchant := receiver.get('seller_merchant_id', None)) or (merchant := receiver.get('merchant_id', None)):
                merchant = db.merchants.find_one({'_id': merchant})
                sede = db.club.find_one({'_id': merchant.get('sede_principal')})
                email_sede = sede.get('contact-email')
            
            global_vars.extend([{'name': 'email_contacto', 'content': email_sede}])
    
    return send_mail(receiver["email"], global_vars, template, brand, test_mail)


def send_mail(receiver_mail, params, template, brand, test_mail="matias@muvinai.com", send_at=None):
    """ Estructura y envía mail

    :param receiver_mail: mail del receptor
    :type receiver_mail: str
    :param params: lista de objetos que son parámetros a pasar al template
    :type params: list
    :param template: nombre del template
    :type template: str
    :param brand: brand
    :type brand: dict
    :param test_mail: mail del receptor en caso de test
    :type receiver_mail: str
    :param send_at: fecha en la cual se debe enviar el mail
    :type send_at: datetime
    :return: informacion del mail
    :rtype: dict
    """
    print("Enviando mail" + template)

    msg = {
        "from_email": brand["mail_sender_address"],
        "from_name": brand["name"],
        "to": [{"email": test_mail}] if test else [{"email": receiver_mail}],
        "global_merge_vars": params
    }

    try:
        body = {"template_name": template, "template_content": [], "message": msg}
        if send_at:
            body['send_at'] = send_at.strftime('%Y-%m-%d %H:%M:%S')
        response = mailchimp.messages.send_template(body)
        print(response)
        return response[0]
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return {}


def send_mail_carrito_abandonado(receiver_mail, client_name, plan, corporativo, cupon_code, price, brand, send_at=None, test_mail="matias@muvinai.com"):
    """ Enviar mail de carrito abandonado

    :param receiver_mail: email del destinatario
    :type receiver_mail: str
    :param client_name: nombre de cliente del destinatario
    :type client_name: str
    :param plan: plan
    :type plan: dict
    :param corporativo:  corporativo
    :type corporativo: dict
    :param cupon_code: cupon de descuento
    :type cupon_code: str
    :param price: precio del plan
    :type price: int
    :param brand: brand del socio
    :type brand: dict
    :param send_at: fecha en la cual se debe enviar el mail
    :type send_at: datetime
    :return: informacion del mail
    :rtype: dict
    """
    url_slug = corporativo['slug'] if corporativo else plan['slug']
    if cupon_code:
        url = f"https://www.sportclub.pagar.club/paso2/{url_slug}?code={cupon_code}&utm_source=checkout&utm_medium=email&utm_campaign=carrito_abandonado"
    else:
        url = f"https://www.sportclub.pagar.club/paso2/{url_slug}?utm_source=checkout&utm_medium=email&utm_campaign=carrito_abandonado"
    global_vars = [
        {"name": "corpo", "content": corporativo.get('slug') if corporativo else None},
        {"name": "name", "content": client_name},
        {"name": "plan", "content": plan['name']},
        {"name": "price", "content": price},
        {"name": "the_url", "content": url}
    ]
    if brand["name"] != "SportClub":
        return

    template = "carrito-abandonado"
    return send_mail(receiver_mail, global_vars, template, brand, send_at=send_at, test_mail=test_mail)


def cancel_scheduled_email(email_id: str):
    """ Enviar mail de carrito abandonado

    :param email_id: id del email a cancelar
    :type email_id: str
    :return: informacion del email cancelado
    :rtype: dict
    """
    try:
        response = mailchimp.messages.cancel_scheduled({'id': email_id})
        print(response)
        return response
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return {}


def cancel_all_scheduled_email_from(email: str):
    """ Enviar mail de carrito abandonado

    :param email: email del destinatario
    :type email: str
    :return: lista de emails cancelados
    :rtype: list
    """
    canceled = []
    emails = mailchimp.messages.list_scheduled({'to': email})
    if isinstance(emails, list):
        for e in emails:
            canceled.append(cancel_scheduled_email(e['_id']))
    return canceled


def send_mail_cambio_tarjeta(receiver, brand, email_contacto=None):
    """ Enviar mail indicando al cliente que debe cambiar la tarjeta.

            :param receiver: documento de cliente del destinatario
            :type receiver: dict
            :param brand: brand
            :type brand: dict
            :param email_contacto: email de contacto de la sede
            :type email_contacto: str
            :return: informacion del mail
            :rtype: dict
            """
    fecha_vigencia = receiver["fecha_vigencia"].strftime("%d/%m/%Y")
    global_vars = [{"name": "nombre", "content": receiver["nombre"]},
                   {"name": "fecha_vigencia", "content": fecha_vigencia},
                   {"name": "email_contacto", "content": email_contacto if email_contacto else brand["email_contacto"]}
                   ]

    if brand["name"].lower() == "sportclub":
        template = "pago-rechazado"
    elif brand["name"].lower() == "aranceles":
        return
    elif brand["name"].upper() == "AON":
        template = "cambio_de_tarjeta_aon"
        global_vars = [
            {'name': 'nombre', 'content': receiver['name']},
        ]
    else:
        template = "pago-rechazado-nosc"
        global_vars.extend([
            {"name": "horizontal_white", "content": brand['images']["horizontal_white"]},
            {"name": "image_dark", "content": brand['images']["image_dark"]},
            {"name": "image_light", "content": brand['images']["image_light"]},
            {"name": "brand_name", "content": brand["name"]},
            {"name": "email_contacto", "content": brand["email_contacto"]}
        ])

    return send_mail(receiver["email"], global_vars, template, brand)


def send_mail_bienvenida(receiver, plan, brand, test_mail="ignacio@muvinai.com"):
    """ Enviar mail de bienvenida a la suscripción.

            :param receiver: documento de cliente del destinatario
            :type receiver: dict
            :return: informacion del mail
            :rtype: dict
            """

    global_vars = [{"name": "nombre", "content": receiver["nombre"]},
                   {"name": "apellido", "content": receiver["apellido"]},
                   {"name": "documento", "content": receiver["documento"]},
                   {"name": "plan", "content": plan["name"]},
                   {"name": "fecha_subscripcion", "content": today_argentina().strftime("%d/%m/%Y")},
                   ]

    if plan["sede_local"]:
        db = init_mongo()
        sede = db.club.find_one({"_id": plan["sede_local"]})
        global_vars.extend([
            {"name": "direccion", "content": sede["direccion"]},
            {"name": "telefono", "content": sede["telefono"]},
            {"name": "contact-email", "content": sede["contact-email"]}
        ])
        if "instagram" in sede.keys():
            global_vars.append({"name": "instagram", "content": sede["instagram"]})

    if brand["name"].lower() == 'sportclub':
        if plan["nivel_de_acceso"] == "Full" or plan["nivel_de_acceso"] == "Flex":
            template = "workclub-bienvenida"
        elif plan["nivel_de_acceso"] == "Local":
            template = "bienvenida-local"
        else:
            template = "bienvenida"
    else:
        template = "bienvenida-nosc"
        global_vars.extend([
            {"name": "logo_mails", "content": brand['images']['mail_logo']},
            {"name": "brand_name", "content": brand["name"]},
            {"name": "email_contacto", "content": brand["email_contacto"]}
        ])

    return send_mail(receiver["email"], global_vars, template, brand, test_mail)


def send_mail_exitoso(receiver, plan, brand):
    global_vars = [{"name": "nombre", "content": receiver["nombre"]},
                   {"name": "apellido", "content": receiver["apellido"]},
                   {"name": "plan", "content": plan["name"]},
                   {"name": "fecha_subscripcion", "content": today_argentina().strftime("%d/%m/%Y")}
                   ]

    if brand["name"].lower() == "sportclub":
        template = "exitoso"
    else:
        template = "exitoso-nosc"
        global_vars.extend([
            {"name": "logo_mails", "content": brand['images']["mail_logo"]},
            {"name": "brand_name", "content": brand["name"]},
            {"name": "email_contacto", "content": brand["email_contacto"]}
        ])

    return send_mail(receiver["email"], global_vars, template, brand)


def send_mail_checkout_rechazado(receiver, plan, brand):
    global_vars = [
        {"name": "nombre", "content": receiver["nombre"]},
        {"name": "slug", "content": plan["slug"]},
        {"name": "email_contacto", "content": brand["email_contacto"]}
    ]

    if brand["name"].lower() == "sportlub":
        template = "checkout-rechazado"
    else:
        template = "checkout-rechazado-nosc"
        global_vars.extend([
            {"name": "logo_mails", "content": brand['images']["mail_logo"]},
            {"name": "brand_name", "content": brand["name"]},
            {"name": "email_contacto", "content": brand["email_contacto"]}
        ])

    return send_mail(receiver["email"], global_vars, template, brand)


def send_mail_pago_en_efectivo(receiver, brand, final_price, plan_name):
    """ Estructura y envía mail
    :param receiver_mail: mail del receptor
    :type receiver_mail: str
    :param test_mail: mail del receptor en caso de test
    :type receiver_mail: str
    :return: informacion del mail
    :rtype: dict
    """
    global_vars = [
        {
            "name": "nombre",
            "content": receiver["nombre"],
        }, {
            "name": "precio_total",
            "content": final_price
        }, {
            "name": "plan",
            "content": plan_name
        }
    ]
    if brand["name"].lower() == "sportclub":
        template = "nueva-boleta"
    else:
        template = "nueva-boleta-nosc"
        global_vars.extend([
            {"name": "logo", "content": brand['images']["mail_logo"]},
            {"name": "brand_name", "content": brand["name"]},
            {"name": "email_contacto", "content": brand["email_contacto"]}
        ])
    return send_mail(receiver["email"], global_vars, template, brand)


def send_mail_pago_pendiente(receiver, brand, test_mail="ignacio@muvinai.com"):
    """ Estructura y envía mail
        :param receiver_mail: mail del receptor
        :type receiver_mail: str
        :param test_mail: mail del receptor en caso de test
        :type receiver_mail: str
        :return: informacion del mail
        :rtype: dict
        """

    global_vars = [{"name": "nombre", "content": receiver["nombre"]}]
    if brand["name"].lower() == "sportclub":
        template = "pago-pendiente"
    else:
        template = "pago-pendiente-nosc"
        global_vars.extend([
            {"name": "logo", "content": brand['images']["mail_logo"]},
            {"name": "brand_name", "content": brand["name"]},
            {"name": "email_contacto", "content": brand["email_contacto"]}
        ])
    return send_mail(receiver["email"], global_vars, template, brand)


def send_mail_cambio_tarjeta_aon(receiver, brand):
    """ Enviar mail indicando al cliente que debe cambiar la tarjeta.

            :param receiver: documento de cliente del destinatario
            :type receiver: dict
            :return: informacion del mail
            :rtype: dict
            """
    template = "cambio-de-tarjeta-aon"
    global_vars = [
        {'name':'nombre','content':receiver['name']},
    ]

    return send_mail(receiver["email"], global_vars, template, brand)


def send_mail_vencimiento_anual(receiver, brand):
    """ Enviar mail indicando al cliente que debe cambiar la tarjeta.

            :param receiver: documento de cliente del destinatario
            :type receiver: dict
            :return: informacion del mail
            :rtype: dict
            """
    template = "vencimiento-anual"
    global_vars = [
        {"name": "nombre", "content": receiver["nombre"]},
        {"name": "apellido", "content": receiver["apellido"]},
        {"name": "plan", "content": receiver["plan"]["name"]},
        {"name": "fecha_vigencia", "content": receiver["fecha_vigencia"].strftime("%d/%m/%Y")},
    ]
    return send_mail(receiver["email"], global_vars, template, brand)


def send_mail_cambio_plan_herenecia(receiver, brand):
    """ Estructura y envía mail
        :param receiver_mail: mail del receptor
        :type receiver_mail: str
        :param test_mail: mail del receptor en caso de test
        :type receiver_mail: str
        :return: informacion del mail
        :rtype: dict
        """
    template = "vencimiento-anual-herencia"
    global_vars = [
        {"name": "nombre", "content": receiver["nombre"]},
        {"name": "apellido", "content": receiver["apellido"]},
        {"name": "precio_mensual", "content": receiver["plan"]['price']},
        {"name": "plan", "content": receiver["plan"]["name"]},
        {"name": "plan_herencia", "content": receiver["plan_herencia"]["name"]},
        {"name": "fecha_vigencia", "content": receiver["fecha_vigencia"].strftime("%d/%m/%Y")},
        {"name": "precio_plan_herencia", "content": receiver['plan_herencia']['price']},
        {"name": "frecuencia", "content": receiver['plan_herencia']['cobro'].lower()}
    ]
    return send_mail(receiver["email"], global_vars, template, brand)


def send_mail_baja(receiver, brand, template):
    """ Enviar mail indicando al cliente que está en estado baja.

        :param receiver: documento de cliente del destinatario
        :type receiver: dict
        :return: informacion del mail
        :rtype: dict
        """
    planes_url = 'https://www.sportclub.com.ar/#planes'
    global_vars = [{"name": "nombre", "content": receiver["nombre"]},
                   {"name": "checkout_link", "content": planes_url}]

    return send_mail(receiver["email"], global_vars, template, brand)