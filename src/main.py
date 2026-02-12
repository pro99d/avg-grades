import flet as ft


def main(page: ft.Page):
    button_theme = ft.ButtonStyle(ft.Colors.BLACK, ft.Colors.BLUE_500)
    text_theme = ft.TextStyle(20)
    grades: list[tuple[ft.TextField, ft.TextField]] = []
    def add_grade(e):
        row = ft.Row()
        def delete(e):
            page.remove(row)
            grades.remove((grade_txt, weight))
            page.update()
        grade_txt = ft.TextField(label= "Оценка", value= "4", on_change= calculate)
        weight = ft.TextField(label= "Вес", value= "1", on_change= calculate)
        delete_btn = ft.IconButton(icon= ft.icons.Icons.DELETE, on_click= delete)
        row.controls = [grade_txt, weight, delete_btn]
        grades.append((grade_txt, weight))
        print("added")
        page.insert(0, row)
        page.update()

    label_vt = ft.Text(value= "Средний балл: ", style= text_theme)
    label_result = ft.Text(value= "", style= text_theme)
    def calculate(e):
        gr = 0
        w = 0
        for grade_txt, weight_txt in grades:
            try:
                g = float(grade_txt.value)
                weight = float(weight_txt.value)
                gr += g
                w += weight
            except ValueError:
                pass
        try:
            label_result.value = str(gr/w)
            label_result.update()
        except ZeroDivisionError:
            pass
        
    for _ in range(3):
        add_grade(0)

    row = ft.Row()
    add_grade = ft.TextButton(content= ft.Text(value= "Добавить оценку", style= text_theme), style= button_theme, on_click= add_grade)
    calculate_btn = ft.TextButton(content= ft.Text(value=" Посчитать", style= text_theme), style= button_theme, on_click= calculate)

    row.controls = [add_grade, calculate_btn, label_vt, label_result] 
    
    page.add(
        ft.SafeArea(
            expand=False,
            content=ft.Container(
                content=row,
                alignment=ft.Alignment.CENTER,
            ),
        )
    )
    calculate(0)


ft.run(main)
