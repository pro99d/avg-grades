import flet as ft

def main(page: ft.Page):
    button_theme = ft.ButtonStyle(ft.Colors.BLACK, ft.Colors.BLUE_500)
    text_theme = ft.TextStyle(15)
    grades: list[tuple[ft.TextField, ft.TextField]] = []
    main_col = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=180)

    label_vt = ft.Text(value="Средний балл: ", style=text_theme)
    label_result = ft.Text(value="", style=text_theme)

    def calculate(e=None):
        gr = 0.0
        w = 0.0
        for grade_txt, weight_txt in grades:
            try:
                g = float(grade_txt.value)
                weight = float(weight_txt.value)
            except Exception:
                continue
            gr += g * weight
            w += weight
        if w == 0:
            label_result.value = ""
        else:
            label_result.value = f"{gr / w:.2f}"
        # Only update the control if it's already added to the page
        if label_result.page:
            label_result.update()
        page.update()

    def add_grade(e=None):
        row = ft.Row()

        def delete(ev=None):
            # remove row from column
            if row in main_col.controls:
                main_col.controls.remove(row)
            # remove corresponding pair from grades
            for i, (gt, wt) in enumerate(grades):
                if gt is grade_txt and wt is weight_txt:
                    grades.pop(i)
                    break
            calculate()
            page.update()

        grade_txt = ft.TextField(label="Оценка", value="4", on_change=calculate, width=100)
        weight_txt = ft.TextField(label="Вес", value="1", on_change=calculate, width=100)
        delete_btn = ft.IconButton(icon=ft.icons.Icons.DELETE, on_click=delete)
        row.controls = [grade_txt, weight_txt, delete_btn]
        grades.append((grade_txt, weight_txt))
        main_col.controls.insert(0, row)
        page.update()

    # create initial rows without calling calculate inside add_grade
    for _ in range(3):
        add_grade()

    # Bottom controls
    row = ft.Row()
    row2 = ft.Row()
    add_btn = ft.TextButton(
        content=ft.Text(value="Добавить оценку", style=text_theme),
        style=button_theme,
        on_click=add_grade,
        width=140,
    )

    row.controls = [add_btn, calculate_btn]
    row2.controls = [label_vt, label_result]

    # Add everything to page first, then run an initial calculation
    page.add(main_col)
    page.add(row)
    page.add(row2)
    calculate()

ft.run(main)

