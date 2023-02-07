#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>

namespace Ui {
class Widget;
}

class Widget : public QWidget
{
   Q_OBJECT


public:
   explicit Widget(QWidget *parent = 0);
   ~Widget();

private slots:

    void on_help_released();

    void on_pushButton__released();

    void on_pushButton_released();

    void on_pushButton_qx_released();

    void on_pushButton_5_released();

    void on_pushButton_6_released();

    void on_help_2_released();

private:
   Ui::Widget *ui;
};

#endif // WIDGET_H
