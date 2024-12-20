from flask import Flask, render_template, request
from processing import get_prediction
import datetime
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["get", "post"])
def index():

    message = ""

    if (request.method == "POST"):
        receive_date = str(request.form.get("receive_date"))
        receive_time = str(request.form.get("receive_time"))
        client_order = int(request.form.get("qty"))
        output_date = str(request.form.get("output_date"))
        output_time = str(request.form.get("output_time"))
        qty = int(request.form.get("qty"))
        supply_volume = int(request.form.get("supply_volume"))

        if not (datetime.strptime(receive_date, "%d-%m-%Y")):
            return "Ошибка. Введите Дату приёмки в формате дд-мм-гггг"
        
        if (len(output_date) > 0):
            output_date_obj = datetime.strptime(output_date, "%d-%m-%Y")
        else:
            output_date_obj = False
        
        # Для не клиентских заказов дата выдачи и время выдачи должны быть пустыми
        if (client_order == 1 & (not bool(output_date_obj))):
            return "Ошибка. Введите Дату выдачи заказа клиенту в бутике в формате дд-мм-гггг"
        
        # return output_date_obj
        
        receive_time_obj = datetime.strptime(receive_time, '%H:%M')

        if (bool(receive_time_obj) == False):
            return "Ошибка. Введите Время Приёмки в формате чч:мм"
        
        if (len(output_time) == 0):
            output_time = 0
        
        # Время выдачи клиенту дальше используется как int
        if ((client_order == 1) & (output_time == 0)):
            return "Ошибка. Введите Время выдачи заказа клиенту в формате чч:мм"
        
        if ((client_order == 0) & (output_time != 0 | bool(output_date_obj))):
            return "Ошибка. Для не клиентских заказов не нужно указывать время и дату выдачи клиенту в бутике"

        if ((client_order == 1) & (receive_date == output_date)):
            output_today = 1
        else:
            output_today = 0

        # Преобразуем время приёмки в float-тип
        time_float = receive_time_obj.hour + round(receive_time_obj.minute / 60, 1)

        predictions = get_prediction(qty, time_float, output_today, output_time, supply_volume)
        message = f"Прогнозируемый день доставки : {predictions["delivery_day"]}. Прогнозируемая поездка : №{predictions["ride_number"]}"

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run()