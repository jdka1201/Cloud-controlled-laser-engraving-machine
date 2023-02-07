#include "Widget.h"
#include "ui_Widget.h"

Widget::Widget(QWidget *parent) :
   QWidget(parent),
   ui(new Ui::Widget)
{
   ui->setupUi(this);

}

Widget::~Widget()
{
   delete ui;
}


void Widget::on_help_released()
{

}

void Widget::on_pushButton__released()
{

}

void Widget::on_pushButton_released()
{

}

void Widget::on_pushButton_qx_released()
{

}

void Widget::on_pushButton_5_released()
{

}

void Widget::on_pushButton_6_released()
{

}

void Widget::on_help_2_released()
{

}
