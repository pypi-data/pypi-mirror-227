import os
from pathlib import Path
from PySide.QtCore import Qt, QObject, QEvent
from PySide.QtGui import QApplication
from PySide import QtGui, QtCore
from ..i18n import translate
from ..machine import Machine
from ..feeds import FeedCalc
from ..feeds.operation import operations, Drilling, Slotting
from ..feeds.material import materials
from ..units import convert
from .util import load_ui
from .spinbox import DistanceSpinBox
from .machineeditor import MachineEditor

__dir__ = os.path.dirname(__file__)
ui_path = os.path.join(__dir__, "feedsandspeeds.ui")
pool = QtCore.QThreadPool()
pool.setMaxThreadCount(1)
active_worker = None

class CalculatorCancelled(Exception):
    pass

class FeedCalculatorWorker(QtCore.QObject):
    finished = QtCore.Signal()
    progress = QtCore.Signal(int)

    def __init__(self, fc):
        super(FeedCalculatorWorker, self).__init__()
        self.fc = fc
        self.result = None

    def start(self):
        def progress_cb(percent):
            if active_worker != self:
                raise CalculatorCancelled()
            return self.progress.emit(percent*100)
        self.result = self.fc.start(progress_cb=progress_cb)
        self.finished.emit()

class FeedCalculatorRunnable(QtCore.QRunnable):
    def __init__(self, fc):
        super(FeedCalculatorRunnable, self).__init__()
        self.setAutoDelete(True)
        self.worker = FeedCalculatorWorker(fc)

    def run(self):
        try:
            self.worker.start()
        except CalculatorCancelled:
            pass

class KeyPressFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() != QEvent.KeyPress:
            return super().eventFilter(obj, event)
        control_modifier = event.modifiers()&Qt.KeyboardModifier.ControlModifier
        if event.key() == Qt.Key.Key_C and control_modifier:
            copied_cells = sorted(obj.selectedIndexes())
            copy_text = ''
            max_column = copied_cells[-1].column()
            for c in copied_cells:
                copy_text += obj.item(c.row(), c.column()).text()
                if c.column() == max_column:
                    copy_text += '\n'
                else:
                    copy_text += '\t'
            QApplication.instance().clipboard().setText(copy_text)
            return True
        return super().eventFilter(obj, event)

warning_dismissed = False

class FeedsAndSpeedsWidget(QtGui.QWidget):
    def __init__(self, db, serializer, tool, parent=None):
        super(FeedsAndSpeedsWidget, self).__init__(parent)
        self.db = db
        self.serializer = serializer
        self.tool = tool
        self.show_internal_results = False

        self.layout = QtGui.QVBoxLayout(self)
        self.setLayout(self.layout)
        self.form = load_ui(ui_path, self, custom_widgets=(DistanceSpinBox,))
        self.layout.addWidget(self.form)

        header = self.form.tableWidget.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        policy = self.form.resultWidget.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.form.resultWidget.setSizePolicy(policy)
        self.form.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.form.tableWidget.customContextMenuRequested.connect(self._on_result_right_click)

        self.form.toolButtonAddMachine.clicked.connect(self._on_new_machine_clicked)
        self.form.toolButtonEditMachine.clicked.connect(self._on_edit_machine_clicked)
        self.form.comboBoxMachine.currentIndexChanged.connect(self._on_machine_selected)
        self.form.comboBoxMaterial.activated.connect(self._on_material_selected)
        self.form.comboBoxOperation.activated.connect(self._on_operation_selected)
        self.form.doubleSpinBoxStickout.valueChanged.connect(self._on_stickout_changed)

        self.form.checkBoxDocLimit.stateChanged.connect(lambda x: self.update_state())
        self.form.doubleSpinBoxDocLimit.valueChanged.connect(lambda x: self.update_state())
        self.form.checkBoxWocLimit.stateChanged.connect(lambda x: self.update_state())
        self.form.doubleSpinBoxWocLimit.valueChanged.connect(lambda x: self.update_state())

        self.form.toolButtonWarning.clicked.connect(self._on_warning_dismissed)
        self.form.toolButtonError.clicked.connect(self.form.errorBox.hide)

        key_press_filter = KeyPressFilter(self)
        self.form.tableWidget.installEventFilter(key_press_filter)

    def _on_warning_dismissed(self):
        self.form.warningBox.hide()
        global warning_dismissed
        warning_dismissed = True

    def _on_machine_selected(self, index):
        self.update_state()

    def _on_material_selected(self, index):
        self.update_state()

    def _on_operation_selected(self, index):
        self.update_state()

    def _on_stickout_changed(self, value):
        self.tool.set_stickout(value, self.form.doubleSpinBoxStickout.unit)
        self.update_state()

    def _on_result_right_click(self, pos):
        menu = QtGui.QMenu(self.form.tableWidget)
        label = translate('btl', 'Show internal properties')
        action = QtGui.QAction(label, self.form.tableWidget, checkable=True)
        action.setChecked(self.show_internal_results)
        action.triggered.connect(self._on_internal_properties_toggled)
        menu.addAction(action)
        menu.exec_(self.form.tableWidget.mapToGlobal(pos))

    def _on_internal_properties_toggled(self, checked):
        self.show_internal_results = checked
        self.update_state()

    def update(self):
        # Update the library dropdown menu.
        combo = self.form.comboBoxMachine
        index = combo.currentIndex()
        combo.clear()
        machines = sorted(self.db.get_machines(), key=lambda l: l.label)
        for machine in machines:
            combo.addItem(machine.label, machine.id)
        combo.setCurrentIndex(index)
        if combo.currentIndex() == -1:
            combo.setCurrentIndex(0)

        combo = self.form.comboBoxMaterial
        index = combo.currentIndex()
        combo.clear()
        material_list = sorted(materials, key=lambda m: m.name)
        for material in material_list:
            combo.addItem(material.name, material)
        combo.setCurrentIndex(index)
        if combo.currentIndex() == -1:
            combo.setCurrentIndex(0)

        combo = self.form.comboBoxOperation
        index = combo.currentIndex()
        combo.clear()
        operation_list = sorted(operations, key=lambda o: o.label())
        for operation in operation_list:
            combo.addItem(operation.label(), operation)
        combo.setCurrentIndex(index)
        if combo.currentIndex() == -1:
            combo.setCurrentIndex(0)

        self.form.warningBox.setVisible(not warning_dismissed)
        # Updating the stickout also triggers .update_state()
        stickout = self.tool.get_stickout_param()
        self.form.doubleSpinBoxStickout.setValueFromParam(stickout)

    def show_hint(self, hint):
        self.form.hintLabel.setText(f"<i>{hint}</i>")
        self.form.hintLabel.show()

    def get_doc_limit(self):
        if not self.form.boxDocLimit.isVisible():
            return None
        if not self.form.checkBoxDocLimit.isChecked():
            return None
        value = self.form.doubleSpinBoxDocLimit.value()
        return convert(value, self.form.doubleSpinBoxDocLimit.unit, 'mm')[0]

    def get_woc_limit(self):
        if not self.form.boxWocLimit.isVisible():
            return None
        if not self.form.checkBoxWocLimit.isChecked():
            return None
        value = self.form.doubleSpinBoxWocLimit.value()
        return convert(value, self.form.doubleSpinBoxWocLimit.unit, 'mm')[0]

    def update_state(self):
        self.form.errorBox.hide()
        self.form.shapePixmap.hide()
        self.form.resultWidget.hide()
        machine = self.get_selected_machine()
        self.form.toolButtonEditMachine.setEnabled(machine is not None)

        op = self.form.comboBoxOperation.currentData()
        self.form.labelDocLimit.setVisible(op != Drilling)
        self.form.boxDocLimit.setVisible(op != Drilling)
        self.form.doubleSpinBoxDocLimit.setEnabled(self.form.checkBoxDocLimit.isChecked())
        self.form.labelWocLimit.setVisible(op not in (Drilling, Slotting))
        self.form.doubleSpinBoxWocLimit.setEnabled(self.form.checkBoxWocLimit.isChecked())
        self.form.boxWocLimit.setVisible(op not in (Drilling, Slotting))

        material = self.get_selected_material()
        stickout = self.form.doubleSpinBoxStickout.value()

        if not machine:
            hint = translate('btl', 'Please select a machine.')
            return self.show_hint(hint)
        elif not material:
            hint = translate('btl', 'Please select a material.')
            return self.show_hint(hint)
        elif not stickout:
            hint = translate('btl', 'Please enter the stickout of the tool.')
            return self.show_hint(hint)
        elif not self.tool.shape.get_flutes():
            hint = translate('btl', 'Tool needs to have more than zero flutes.')
            return self.show_hint(hint)
        elif not self.tool.supports_feeds_and_speeds():
            hint = translate('btl', 'Tool shape not supported by the calculator.')
            return self.show_hint(hint)
        self.form.hintLabel.hide()

        # Prepare the calculator.
        fc = FeedCalc(machine, self.tool, material, op=op)
        error = fc.get_error()
        if error:
            hint = translate('btl', 'Calculator error: {error}')
            return self.show_hint(hint.format(error=error))

        # Apply limits, if any.
        doc_limit = self.get_doc_limit()
        fc.doc.max = doc_limit if doc_limit else fc.doc.max
        woc_limit = self.get_woc_limit()
        fc.woc.max = woc_limit if woc_limit else fc.woc.max

        # Calculate.
        pool.clear()
        runnable = FeedCalculatorRunnable(fc)
        global active_worker
        active_worker = runnable.worker
        active_worker.finished.connect(pool.releaseThread)
        active_worker.progress.connect(self._on_calculator_progress)
        active_worker.finished.connect(lambda: self._on_calculator_finished(runnable.worker))
        pool.start(runnable)

    def _on_calculator_progress(self, progress):
        self.form.progressBar.setValue(progress)
        self.form.progressBar.show()

    def _on_calculator_finished(self, worker):
        # Unfortunately QThreadPool.activeThreadCount() is currently broken,
        # see https://bugreports.qt.io/browse/QTBUG-21051
        # Leaving this disabled; the user may see multiple updates that way,
        # but not a big deal.
        #if pool.activeThreadCount() > 0:
        #    return
        self.form.progressBar.hide()
        error, params = worker.result
        if error is not None:
            text = translate('btl', 'No valid result found. Best result has error: {error}')
            self.form.labelError.setText(text.format(error=error))
            self.form.errorBox.show()
        else:
            self.form.errorBox.hide()

        # Show the result.
        self.form.warningBox.setVisible(not warning_dismissed)
        self.form.resultWidget.show()
        rpm = params.get('rpm')
        none_text = translate('btl', 'none')
        none_text = f'<i>{none_text}</i>'
        self.form.rpmResultLabel.setText(rpm.format() if rpm else none_text)
        feed = params.get('feed')
        self.form.feedResultLabel.setText(feed.format() if feed else none_text)
        diameter = self.tool.shape.get_diameter()
        woc = params.get('woc')
        woc_label = f'{woc.format()} ({woc.v/diameter*100:.3f}%)' if woc else None
        self.form.stepoverResultLabel.setText(woc_label if woc else none_text)
        doc = params.get('doc')
        self.form.stepdownResultLabel.setText(doc.format() if doc else none_text)

        if not self.show_internal_results:
            params = {k: v for k, v in params.items() if not v.is_internal}

        table = self.form.tableWidget
        table.clear()
        table.setRowCount(len(params))
        params = sorted(params.items(), key=lambda x: x[0].lower())
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        for row, (name, param) in enumerate(params):
            # First column: Name.
            label = name.replace('_', ' ').title()
            item = QtGui.QTableWidgetItem(label)
            font.setItalic(param.is_internal)
            item.setFont(font)
            table.setItem(row, 0, item)

            # Second column: Values and limits, marked if near the limit.
            item = QtGui.QTableWidgetItem(param.to_string())
            percent = param.get_percent_of_limit()*100
            if not param.within_minmax():
                 item.setForeground(QtGui.QColor(255, 255, 255))
                 item.setBackground(QtGui.QColor(255, 0, 0, 255))
            elif percent >= 95:
                 item.setBackground(QtGui.QColor(255, 165, 0))
            table.setItem(row, 1, item)

        # Display the shape.
        self.form.shapePixmap.show()
        tool_pixmap = self.tool.get_pixmap()
        img_data = tool_pixmap.render_engagement(doc.v, woc.v)
        image = QtGui.QImage(img_data,
                             tool_pixmap.size,
                             tool_pixmap.size,
                             QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.form.shapePixmap.setPixmap(pixmap)

    def get_selected_machine(self):
        machine_id = self.form.comboBoxMachine.currentData()
        if not machine_id:
            return
        return self.db.get_machine_by_id(machine_id)

    def get_selected_material(self):
        return self.form.comboBoxMaterial.currentData()

    def _show_machine_editor(self, machine):
        editor = MachineEditor(self.db, self.serializer, machine, self)
        if not editor.exec():
            return
        self.db.add_machine(machine)
        self.db.serialize_machines(self.serializer)
        self.update()

    def _on_new_machine_clicked(self):
        self._show_machine_editor(Machine())

    def _on_edit_machine_clicked(self):
        machine = self.get_selected_machine()
        self._show_machine_editor(machine)
