from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
import os
import re

drafting_bp = Blueprint('drafting', __name__)

@drafting_bp.route('/redactar')
@login_required
def select_document():
    # En el futuro, aquí podrías listar varias plantillas
    return render_template('select_document.html')

@drafting_bp.route('/redactar/contrato_arrendamiento', methods=['GET', 'POST'])
@login_required
def draft_arrendamiento():
    template_path = os.path.join('document_templates', 'contrato_arrendamiento_template.txt')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Usamos una expresión regular para encontrar todos los marcadores {{...}}
    placeholders = re.findall(r'{{(.*?)}}', template_content)

    if request.method == 'POST':
        # Cuando el usuario envía el formulario
        document_data = request.form.to_dict()
        final_document = template_content
        for key, value in document_data.items():
            final_document = final_document.replace(f'{{{{{key}}}}}', value)

        return render_template('documento_generado.html', document_content=final_document)

    # Si es GET, mostramos el formulario
    return render_template('redactar_form.html', placeholders=placeholders)