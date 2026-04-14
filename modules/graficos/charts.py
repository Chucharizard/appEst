def process_chart_data(form_data):
    """
    Recibe el ImmutableMultiDict o dict del request.form y devuelve
    (chart_data, error_message).
    """
    chart_data = None
    error_message = None

    chart_type = form_data.get('chart_type')
    raw_labels = form_data.get('labels')
    raw_values = form_data.get('values')
    raw_values2 = form_data.get('values2')

    if not raw_labels or not raw_values:
        error_message = "Por favor, completa los campos requeridos (Categorías y Valores Grupo 1)."
        return chart_data, error_message

    try:
        labels = [label.strip() for label in raw_labels.split(',')]
        values = [float(val.strip()) for val in raw_values.split(',')]

        values2 = None
        if raw_values2 and raw_values2.strip():
            values2 = [float(val.strip()) for val in raw_values2.split(',')]

        if len(labels) != len(values):
            error_message = f"Error: Hay {len(labels)} categorías pero {len(values)} valores en el Grupo 1. Deben coincidir."
        elif values2 and len(labels) != len(values2):
            error_message = f"Error: Hay {len(labels)} categorías pero {len(values2)} valores en el Grupo 2. Deben coincidir."
        else:
            color_principal = '#7c5cfc' # Var accent
            color_secundario = '#ec4899' # Pink
            paleta_multiple = ['#7c5cfc', '#ec4899', '#2bcc96', '#22d3ee', '#8b5cf6', '#3b82f6', '#ef4444']

            chart_js_type = 'bar'
            index_axis = 'x'
            bg_color = color_principal + '99'
            border_color = color_principal
            extra_options = {}
            is_stacked = False
            datasets = []

            if chart_type == 'burbujas':
                chart_js_type = 'bubble'
                bubble_data = [
                    {'x': i + 1, 'y': values[i], 'r': values2[i] if values2 else 15}
                    for i in range(len(values))
                ]
                datasets.append({
                    'label': 'Volumen',
                    'data': bubble_data,
                    'originalLabels': labels,
                    'backgroundColor': paleta_multiple[0] + '80',
                    'borderColor': paleta_multiple[0],
                    'borderWidth': 2,
                })

            elif chart_type == 'compuestas':
                chart_js_type = 'bar'
                is_stacked = True
                datasets.append({
                    'label': 'Segmento A', 'data': values,
                    'backgroundColor': paleta_multiple[0] + 'AA',
                    'borderColor': paleta_multiple[0], 'borderWidth': 1
                })
                if values2:
                    datasets.append({
                        'label': 'Segmento B', 'data': values2,
                        'backgroundColor': paleta_multiple[1] + 'AA',
                        'borderColor': paleta_multiple[1], 'borderWidth': 1
                    })

            elif chart_type == 'bastones':
                chart_js_type = 'bar'
                datasets.append({
                    'label': 'Frecuencia', 'data': values,
                    'backgroundColor': color_principal,
                    'barThickness': 3, 'borderRadius': 10
                })
                datasets.append({
                    'type': 'scatter', 'label': 'Cima', 'data': values,
                    'backgroundColor': color_secundario,
                    'pointRadius': 6, 'pointHoverRadius': 10
                })

            else:
                if chart_type == 'columnas':
                    chart_js_type = 'bar'
                elif chart_type == 'barras':
                    chart_js_type = 'bar'
                    index_axis = 'y'
                elif chart_type == 'lineal':
                    chart_js_type = 'line'
                    extra_options = {'tension': 0.4, 'fill': False}
                elif chart_type == 'area':
                    chart_js_type = 'line'
                    extra_options = {'tension': 0.4, 'fill': True}
                    bg_color = 'rgba(124, 92, 252, 0.2)'
                elif chart_type == 'puntos':
                    chart_js_type = 'line'
                    extra_options = {'showLine': False, 'pointRadius': 8, 'pointHoverRadius': 12}
                elif chart_type in ['circular', 'dona']:
                    chart_js_type = 'pie' if chart_type == 'circular' else 'doughnut'
                    bg_color = paleta_multiple
                    border_color = 'rgba(255,255,255,0.05)'

                datasets.append({
                    'label': 'Grupo Principal', 'data': values,
                    'backgroundColor': bg_color, 'borderColor': border_color,
                    'borderWidth': 2, **extra_options
                })

                if values2 and chart_type in ['columnas', 'barras', 'lineal', 'area', 'puntos']:
                    datasets.append({
                        'label': 'Comparador (2do Grupo)', 'data': values2,
                        'backgroundColor': paleta_multiple[1] + '99',
                        'borderColor': paleta_multiple[1],
                        'borderWidth': 2, **extra_options
                    })

            chart_data = {
                'type': chart_js_type,
                'labels': labels,
                'datasets': datasets,
                'index_axis': index_axis,
                'title': chart_type.replace('_', ' ').title(),
                'is_stacked': is_stacked
            }

    except ValueError:
        error_message = "Asegúrate de teclear únicamente números en los campos de Valores (ej. 10.5, 20)."

    return chart_data, error_message
