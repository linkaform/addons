# coding: utf-8
"""
OCR Mixin para lkf_addons.
Agrega los métodos de OCR a cualquier clase que herede de Base.

Uso — en accesos_utils.py agregar herencia:

    from lkf_addons.addons.accesos.items.scripts.ocr_mixin import OcrMixin

    class Accesos(OcrMixin, Accesos):
        pass

O si prefieres meterlo directo en Base (base/app.py):

    from lkf_addons.addons.accesos.items.scripts.ocr_mixin import OcrMixin

    class Base(OcrMixin, base.LKF_Base):
        pass
"""


class OcrMixin:
    """
    Métodos de OCR que se apoyan en self.ai (OpenRouter).
    Se mezclan con cualquier clase que herede de LKF_Base,
    donde self.ai es la instancia de OpenRouter (o None si no está configurado).
    """

    # ──────────────────────────────────────────────────────────
    # OCR DE IDENTIFICACIÓN
    # ──────────────────────────────────────────────────────────

    def ocr_articulo_perdido(self, image_source: list,
                            model: str = 'google/gemini-2.5-flash-lite') -> dict:
        """
        Analiza la foto de un artículo perdido y extrae los campos visibles.

        Args:
            image_source: URL remota o ruta local de la imagen.
            model:        Modelo OpenRouter a usar.

        Returns:
            dict con:
                - status_code: 200/400/500
                - data: campos extraídos (nombre, tipo_articulo, color, marca, modelo,
                        descripcion, caracteristicas)
                - msg: mensaje de resultado

        Campos NO extraíbles de la foto (se llenan manualmente en el form):
            ubicacion, area, fecha_hallazgo, area_resguardo, quien_entrega
        """
        system = (
            "Eres un asistente de seguridad de un corporativo encargado de registrar "
            "artículos perdidos o encontrados. Analizas fotos de objetos para describir "
            "sus características de forma precisa y objetiva."
        )
        prompt = (
            "Analiza la foto del artículo y regresa un JSON con los siguientes campos "
            "(usa null si no puedes determinarlo con certeza):\n"
            "- nombre: 'str' Nombre descriptivo breve del objeto (ej. 'Mochila', 'Audífonos', 'Llave USB')\n"
            "- tipo_articulo: 'str' Categoría del objeto. Elige uno de: "
            "Bolsa, Mochila, Cartera, Electrónico, Ropa, Calzado, Llave, Joyería, Documento, Otro\n"
            "- color: 'str' Color principal del artículo\n"
            "- marca: 'str' Marca si es legible en el objeto (ej. Nike, Apple, Samsung), null si no aplica\n"
            "- modelo: 'str' Modelo si es legible (ej. iPhone 14, Galaxy S23), null si no aplica\n"
            "- descripcion: 'str' Descripción general de lo que se ve en la foto\n"
            "- caracteristicas: 'str' Detalles distintivos visibles: stickers, daños, inscripciones, "
            "número de serie, estado de conservación, etc. null si no hay nada relevante"
        )


        if not self.ai:
            return {'status_code': 400, 'msg': 'OpenRouter no configurado'}

        try:
            raw_text = self.ai.ocr_general(image_source, system, prompt, model=model, agent='Clave10: ObjPerdido')
        except ValueError as e:
            return self.LKFException({'status_code': 500, 'msg': f'Error OCR: {e}'})
        except Exception as e:
            return self.LKFException({'status_code': 500, 'msg': f'Error inesperado: {e}'})

        datos = {}
        if raw_text.get('choices'):
            if isinstance(raw_text['choices'], list) and len(raw_text['choices']) > 0:
                if raw_text['choices'][0].get('message', {}).get('content'):
                    datos = raw_text['choices'][0]['message']['content']

        return {'status_code': 200, 'msg': 'OK', 'data': datos}

    def ocr_paquete(self, image_source: list, fields: dict = {},
                           extra_instructions: str = None,
                           model: str = 'google/gemini-2.5-flash-lite') -> dict:
        """
        Extrae los datos de una foto de un paquete para identificar, 
        Proveedor (paqueteria), Remitente, Destinatario.
        Si encuentra un telefono, intenta enviar un sms o whatsapp.
        Si ecuentra un correo intenta enviar un correo.
        Podemos ver si le pudiera marcar y platicado decirle llego tu 
        paquete de MercadoLibre. O llego tu comida.

        Args:
            image_source: URL remota o ruta local de la imagen.
            model:        Modelo OpenRouter a usar (opcional).
            MODEL = "anthropic/claude-haiku-4.5"  # excelente OCR, precio razonable
            MODEL = "google/gemini-2.5-flash"  # un escalón arriba, más caro pero mejor

        Returns:
            dict con:
                - status_code: 200/201/400/500
                - data: campos extraídos por el OCR
                - msg: mensaje de resultado

        Ejemplo de uso en script:
            response = acceso_obj.ocr_paquete(
                image_source="https://s3.../ine.jpg",
            )
        """
        system = (
            "Eres un OCR especializado en Paquetes de entrega. "
            "Eres un guarida de segurida o recepcionista de un gran corportativo que recive"
            "Muchos paquetes, de paqueterias o de comida"
        )
        prompt = (
            "Lee la informacion de la etiqueta proporcionada. Regresa en un JSON los datos de:"
            "- remitente: 'str' Es el remitente, el orgien del paquete, el quien envia. Normalmente esta en letra mas pequeña"
            "- telefono_remitente: 'str' telefono quien envia"
            "- direccion_remiente: es la direccion de quien envia"
            "- destinatario: 'str' Es para quien va el paquete, el receptor. Normalmente esta en lerta mas grande, y es el nombre de una persona"
            "- telefono_receptor: 'str' telefono quien recibe    "
            "- email_receptor: 'str' email quien recibe    "
            "- paqueteria: 'str' Empresa quien envia el paquete, ej FedEx, USPS, UPS, UberEats"
            "- no_guia: 'str' Es el numero de guia o numero de orden o numero de paquete"
            "- telefono_receptor: 'str' Telefono de quien recibe"
            "- tipo_paquete: 'str' indica el tipo de paquete 1 a 3 palabras del tipo de paquete, ya sea caja, bolsa, tubo, etc."
            "- descripcion: 'str' descripcion breve del paquete, con informacion relevante"
            )

        if not self.ai:
            return {'status_code': 400, 'msg': 'OpenRouter no configurado'}

        # 1. Extraer datos con el LLM
        try:
            raw_text = self.ai.ocr_general(image_source, system, prompt, model=model, agent='Clave10: Transportes')
        except ValueError as e:
            return self.LKFException({'status_code': 500, 'msg': f'Error OCR: {e}'})
        except Exception as e:
            return self.LKFException({'status_code': 500, 'msg': f'Error inesperado: {e}'})

        # 2. Normalizar — esto es código, no LLM
        datos = {}
        if raw_text.get('choices'):
            if isinstance(raw_text['choices'], list) and len(raw_text['choices']) >0:
                if raw_text['choices'][0].get('message',{}).get('content'):
                    datos = raw_text['choices'][0]['message']['content']

        datos = self._ocr_normalizar(datos)

        # Se asigna nombre del remitente
        nombre_remitente = datos.get('remitente', '')
        empleados = self.get_employees_names()
        match_empleado = self._match_label(nombre_remitente, empleados)
        if match_empleado.get('label'):
            datos['remitente'] = match_empleado['label']

        # Se asigna nombre del proveedor de paqueteria
        proveedores = self.get_proveedores_paqueteria()
        proveedor = datos.get('paqueteria')
        match_proveedor = self._match_label(proveedor, proveedores)
        if not match_proveedor.get('label'):
            try:
                self.create_proveedor_de_paqueteria(proveedor)
            except:
                datos['paqueteria'] = proveedor
        else:
            datos['paqueteria'] = match_proveedor['label']

        # 3. Validar
        errores = self._ocr_validar_id(datos)
        if errores:
            return {
                'status_code': 206,  # partial content — extrajo pero hay campos inválidos
                'msg': 'Extracción con advertencias',
                'data': datos,
                'warnings': errores,
            }
        return {'status_code': datos.get('status_code', 200), 'msg': 'OK', 'data': datos}

    def ocr_identificacion(self, image_source: str, form_id: int = None,
                           model: str = 'google/gemini-2.5-flash-lite', 
                           name: str = None) -> dict:
        """
        Extrae los datos de una identificación (INE, pasaporte, licencia, etc.)
        y opcionalmente crea el registro en LinkaForm.

        Args:
            image_source: URL remota o ruta local de la imagen.
            form_id:      Si se proporciona, crea el registro en ese formulario.
            model:        Modelo OpenRouter a usar (opcional).
            MODEL = "anthropic/claude-haiku-4.5"  # excelente OCR, precio razonable
            MODEL = "google/gemini-2.5-flash"  # un escalón arriba, más caro pero mejor

        Returns:
            dict con:
                - status_code: 200/201/400/500
                - data: campos extraídos por el OCR
                - folio: folio del registro creado (si se pasó form_id)
                - msg: mensaje de resultado

        Ejemplo de uso en script:
            response = acceso_obj.ocr_identificacion(
                image_source="https://s3.../ine.jpg",
                form_id=self.EMPLEADOS_FORM,
            )
        """

        if not self.ai:
            return {'status_code': 400, 'msg': 'OpenRouter no configurado'}

        # 1. Extraer datos con el LLM
        try:
            raw_text = self.ai.ocr_id(image_source, model=model, name=name)
        except ValueError as e:
            return {'status_code': 500, 'msg': f'Error OCR: {e}'}
        except Exception as e:
            return {'status_code': 500, 'msg': f'Error inesperado: {e}'}

        # 2. Normalizar — esto es código, no LLM
        datos = {}
        if raw_text.get('choices'):
            if isinstance(raw_text['choices'], list) and len(raw_text['choices']) >0:
                if raw_text['choices'][0].get('message',{}).get('content'):
                    datos = raw_text['choices'][0]['message']['content']

        datos = self._ocr_normalizar(datos)

        # 3. Validar
        errores = self._ocr_validar_id(datos)
        if errores:
            return {
                'status_code': 206,  # partial content — extrajo pero hay campos inválidos
                'msg': 'Extracción con advertencias',
                'data': datos,
                'warnings': errores,
            }
        # 4. Crear registro en LinkaForm si se solicitó
        if form_id:
            try:
                result = self._ocr_crear_registro(datos, form_id)
                return {
                    'status_code': 201,
                    'msg': 'Registro creado exitosamente',
                    'data': datos,
                    'folio': result.get('folio'),
                }
            except Exception as e:
                return {
                    'status_code': 500,
                    'msg': f'OCR OK pero error al crear registro: {e}',
                    'data': datos,
                }

        status = 200 if isinstance(datos, list) else datos.get('status_code', 200)
        return {'status_code': status, 'msg': 'OK', 'data': datos}

    # ──────────────────────────────────────────────────────────
    # OCR GENÉRICO
    # ──────────────────────────────────────────────────────────

    def ocr_documento(self, image_source: str, fields: list = None,
                      extra_instructions: str = None, form_id: int = None,
                      model: str = None) -> dict:
        """
        OCR genérico para cualquier tipo de documento.

        Args:
            image_source:       URL remota o ruta local de la imagen.
            fields:             Lista de campos a extraer. Si es vacía, extrae todo.
            extra_instructions: Instrucciones adicionales al modelo.
            form_id:            Si se proporciona, crea el registro en ese formulario.
            model:              Modelo OpenRouter a usar (opcional).

        Returns:
            dict con status_code, data, folio (si aplica), msg.

        Ejemplo:
            response = acceso_obj.ocr_documento(
                image_source="https://s3.../factura.jpg",
                fields=["numero_factura", "total", "rfc_emisor", "fecha"],
            )
        """
        if not self.ai:
            return {'status_code': 400, 'msg': 'OpenRouter no configurado'}

        try:
            datos = self.ai.ocr(
                image_source,
                fields=fields,
                extra_instructions=extra_instructions,
                model=model,
            )
        except ValueError as e:
            return {'status_code': 500, 'msg': f'Error OCR: {e}'}
        except Exception as e:
            return {'status_code': 500, 'msg': f'Error inesperado: {e}'}

        if form_id:
            try:
                result = self._ocr_crear_registro(datos, form_id)
                return {
                    'status_code': 201,
                    'msg': 'Registro creado exitosamente',
                    'data': datos,
                    'folio': result.get('folio'),
                }
            except Exception as e:
                return {
                    'status_code': 500,
                    'msg': f'OCR OK pero error al crear registro: {e}',
                    'data': datos,
                }
        return {'status_code': datos.get('status_code', 200), 'msg': 'OK', 'data': datos}

    # ──────────────────────────────────────────────────────────
    # OCR BATCH
    # ──────────────────────────────────────────────────────────

    def ocr_batch(self, images: list, option_type: str = 'ocr_id',
                  form_id: int = None, model: str = None) -> dict:
        """
        Procesa una lista de imágenes en batch.

        Args:
            images:      Lista de URLs o rutas locales.
            option_type: 'ocr_id' o 'ocr_doc'.
            form_id:     Si se proporciona, crea registros en ese formulario.
            model:       Modelo OpenRouter a usar (opcional).

        Returns:
            dict con resultados por imagen y resumen.

        Ejemplo:
            response = acceso_obj.ocr_batch(
                images=[
                    "https://s3.../ine_juan.jpg",
                    "https://s3.../ine_maria.jpg",
                ],
                option_type='ocr_id',
                form_id=self.EMPLEADOS_FORM,
            )
        """
        if not self.ai:
            return {'status_code': 400, 'msg': 'OpenRouter no configurado'}

        if not images:
            return {'status_code': 400, 'msg': 'Se requiere lista de imágenes'}

        results   = []
        ok_count  = 0
        err_count = 0

        for i, image_source in enumerate(images, start=1):
            print(f"  [{i}/{len(images)}] procesando: {image_source}")
            try:
                if option_type == 'ocr_id':
                    result = self.ocr_identificacion(
                        image_source=image_source,
                        form_id=form_id,
                        model=model,
                    )
                else:
                    result = self.ocr_documento(
                        image_source=image_source,
                        form_id=form_id,
                        model=model,
                    )

                results.append({'source': image_source, **result})
                if result.get('status_code') in (200, 201, 206):
                    ok_count += 1
                else:
                    err_count += 1

            except Exception as e:
                err_count += 1
                results.append({
                    'source': image_source,
                    'status_code': 500,
                    'msg': str(e),
                })

        return {
            'status_code': 200,
            'summary': {
                'total':   len(images),
                'ok':      ok_count,
                'errores': err_count,
            },
            'results': results,
        }

    # ──────────────────────────────────────────────────────────
    # HELPERS PRIVADOS
    # ──────────────────────────────────────────────────────────

    def _match_label(self, nombre: str, empleados: list, umbral: int = 75) -> dict:
        """
        Busca el empleado más parecido a `nombre` usando difflib.
        Normaliza tildes y orden de palabras antes de comparar.

        Returns:
            {'empleado': str, 'score': int}  si supera el umbral
            {'empleado': None, 'score': int}  si ninguno supera el umbral
        """
        import unicodedata
        from difflib import SequenceMatcher

        def normalizar(s):
            s = unicodedata.normalize('NFD', s)
            s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
            return ' '.join(sorted(s.lower().split()))

        nombre_norm = normalizar(nombre)
        nombre_words = set(nombre_norm.split())
        mejor, mejor_score = None, 0

        for emp in empleados:
            emp_norm = normalizar(emp)
            emp_words = set(emp_norm.split())
            seq_score = int(SequenceMatcher(None, nombre_norm, emp_norm).ratio() * 100)
            word_score = int(len(nombre_words & emp_words) / len(nombre_words) * 100) if nombre_words else 0
            score = max(seq_score, word_score)
            if score > mejor_score:
                mejor, mejor_score = emp, score

        if mejor_score >= umbral:
            return {'label': mejor, 'score': mejor_score}
        return {'label': None, 'score': mejor_score}

    def _ocr_normalizar(self, datos):
        """Normaliza los datos extraídos. Código puro, sin LLM."""
        if isinstance(datos, list):
            return [self._ocr_normalizar(d) for d in datos]
        datos['nombre_completo'] = ""
        if datos.get('curp'):
            datos['curp'] = datos['curp'].upper().strip()
        if datos.get('rfc'):
            datos['rfc'] = datos['rfc'].upper().strip()
        if datos.get('nombre'):
            datos['nombre'] = datos['nombre'].strip().title()
            datos['nombre_completo'] += f"{datos['nombre']}"
        if datos.get('apellido_paterno'):
            datos['apellido_paterno'] = datos['apellido_paterno'].strip().title()
            datos['nombre_completo'] += f" {datos['apellido_paterno']}"
        if datos.get('apellido_materno'):
            datos['apellido_materno'] = datos['apellido_materno'].strip().title()
            datos['nombre_completo'] += f" {datos['apellido_materno']}"
        if not datos['nombre_completo']:
            datos.pop('nombre_completo')
        return datos

    def _ocr_validar_id(self, datos) -> list:
        """
        Validaciones deterministas de una ID. Código puro, sin LLM.
        Retorna lista de warnings (vacía = todo OK).
        """
        if isinstance(datos, list):
            return [w for d in datos for w in self._ocr_validar_id(d)]
        import re
        warnings = []

        curp = datos.get('curp')
        if curp and not re.match(r'^[A-Z]{4}\d{6}[HM][A-Z]{5}\d{2}$', curp):
            warnings.append(f'CURP con formato inválido: {curp}')

        rfc = datos.get('rfc')
        if rfc and not re.match(r'^[A-Z]{3,4}\d{6}[A-Z0-9]{3}$', rfc):
            warnings.append(f'RFC con formato inválido: {rfc}')

        fecha = datos.get('fecha_nacimiento')
        if fecha:
            try:
                from datetime import datetime
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                warnings.append(f'fecha_nacimiento con formato inválido: {fecha}')

        return warnings

    def _ocr_crear_registro(self, datos: dict, form_id: int) -> dict:
        """
        Crea el registro en LinkaForm con los datos extraídos.
        Mapea nombre_campo → ObjectId usando self.f
        """
        answers = {}
        for campo, obj_id in self.f.items():
            if datos.get(campo) is not None:
                answers[obj_id] = datos[campo]

        metadata = self.lkf_api.get_metadata(form_id=form_id)
        metadata.update({
            'answers': answers,
            'properties': {
                'device_properties': {
                    'System':  'Addons',
                    'Process': 'OCR',
                    'Action':  'create_from_image',
                }
            }
        })
        return self.lkf_api.post_forms_answers(metadata)