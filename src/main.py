import flet as ft

def main(page: ft.Page):
    page.title = "Калькулятор средневзвешенного балла"
    button_theme = ft.ButtonStyle(ft.Colors.BLACK, ft.Colors.BLUE_500)
    text_theme = ft.TextStyle(15)
    grades: list[tuple[ft.TextField, ft.TextField]] = []
    row_refs: list[tuple[ft.Row, ft.TextField, ft.TextField, ft.IconButton]] = []
    main_col = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    label_vt = ft.Text(value="Средний балл: ", style=text_theme)
    label_result = ft.Text(value="", style=text_theme)
    add_btn = ft.TextButton(
        content=ft.Text(value="Добавить оценку", style=text_theme),
        style=button_theme,
        on_click=lambda e: add_grade(),
    )

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

    def get_layout_settings() -> tuple[int, int, int]:
        width = page.width or page.window.width or 640
        if width < 420:
            return 6, 8, 38
        if width < 720:
            return 10, 12, 40
        return 14, 16, 42

    def apply_layout():
        row_spacing, container_padding, delete_btn_width = get_layout_settings()
        height = page.height or page.window.height or 800
        top_padding = max(container_padding, int(height * 0.07))
        page.padding = ft.padding.only(
            top=top_padding,
            left=container_padding,
            right=container_padding,
            bottom=container_padding,
        )
        main_col.spacing = row_spacing
        for row, grade_txt, weight_txt, delete_btn in row_refs:
            row.spacing = row_spacing
            row.expand = True
            grade_txt.expand = 1
            weight_txt.expand = 1
            delete_btn.width = delete_btn_width
            delete_btn.height = delete_btn_width
        if page.controls:
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
            for i, (r, gt, wt, _) in enumerate(row_refs):
                if r is row and gt is grade_txt and wt is weight_txt:
                    row_refs.pop(i)
                    break
            calculate()
            page.update()

        grade_txt = ft.TextField(label="Оценка", value="4", on_change=calculate, expand=1)
        weight_txt = ft.TextField(label="Вес", value="1", on_change=calculate, expand=1)
        delete_btn = ft.IconButton(icon=ft.icons.Icons.DELETE, on_click=delete)
        row.controls = [grade_txt, weight_txt, delete_btn]
        grades.append((grade_txt, weight_txt))
        row_refs.append((row, grade_txt, weight_txt, delete_btn))
        main_col.controls.insert(0, row)
        apply_layout()
        page.update()

    # create initial rows without calling calculate inside add_grade
    for _ in range(3):
        add_grade()

    # Bottom controls
    add_btn.expand = True
    add_btn_row = ft.Row(
        controls=[add_btn],
        expand=True,
    )
    result_block = ft.Row(
        controls=[label_vt, label_result],
        spacing=8,
        tight=True,
        alignment=ft.MainAxisAlignment.START,
    )
    bottom_panel = ft.Column(
        controls=[add_btn_row, result_block],
        spacing=8,
    )

    def on_resize(e):
        apply_layout()

    page.on_resize = on_resize

    # Add everything to page first, then run an initial calculation
    page.add(main_col)
    page.add(bottom_panel)
    apply_layout()
    calculate()

ft.run(main)

