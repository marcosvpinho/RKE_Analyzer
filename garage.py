#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: RKE Analyzer
# Author: Marcos
# Generated: Sat Oct 27 10:22:58 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy as np
import osmosdr
import sip
import sumx
import sys
import threading
import time
from gnuradio import qtgui


class garage(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "RKE Analyzer")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RKE Analyzer")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "garage")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.sdr_rate = sdr_rate = 1.8e6
        self.freqdetectada = freqdetectada = 0
        self.decim = decim = 10
        self.variable_qtgui_label_0_2 = variable_qtgui_label_0_2 = freqdetectada
        self.sps = sps = 45
        self.samp_rate = samp_rate = sdr_rate / decim
        self.freq = freq = 292000000
        self.fft_n = fft_n = 128

        ##################################################
        # Blocks
        ##################################################
        self.sumx = sumx.summ()
        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, 'Tab 0')
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, 'Tab 1')
        self.top_grid_layout.addWidget(self.tab, 1, 0, 10, 1)
        for r in range(1, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)

        def _freq_probe():
            while True:
                val = self.sumx.freq_ativa()
                try:
                    self.set_freq(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (0.15))
        _freq_thread = threading.Thread(target=_freq_probe)
        _freq_thread.daemon = True
        _freq_thread.start()

        self._variable_qtgui_label_0_2_tool_bar = Qt.QToolBar(self)

        if None:
          self._variable_qtgui_label_0_2_formatter = None
        else:
          self._variable_qtgui_label_0_2_formatter = lambda x: repr(x)

        self._variable_qtgui_label_0_2_tool_bar.addWidget(Qt.QLabel('freeq'+": "))
        self._variable_qtgui_label_0_2_label = Qt.QLabel(str(self._variable_qtgui_label_0_2_formatter(self.variable_qtgui_label_0_2)))
        self._variable_qtgui_label_0_2_tool_bar.addWidget(self._variable_qtgui_label_0_2_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_2_tool_bar)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(sdr_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(10, 0)
        self.rtlsdr_source_0.set_bb_gain(10, 0)
        self.rtlsdr_source_0.set_antenna('00', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)

        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	sdr_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win)

        def _freqdetectada_probe():
            while True:
                val = self.sumx.freq_detectada()
                try:
                    self.set_freqdetectada(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (0.15))
        _freqdetectada_thread = threading.Thread(target=_freqdetectada_probe)
        _freqdetectada_thread.daemon = True
        _freqdetectada_thread.start()

        self.fir_filter_xxx_1 = filter.fir_filter_ccf(decim, (1, ))
        self.fir_filter_xxx_1.declare_sample_delay(0)
        self.fft = fft.fft_vcc(fft_n, True, (window.blackmanharris(fft_n)), True, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, fft_n)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_n)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_n)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.sumx, 0))
        self.connect((self.fft, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.fir_filter_xxx_1, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.fir_filter_xxx_1, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.sumx, 0), (self.blocks_null_sink_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "garage")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sdr_rate(self):
        return self.sdr_rate

    def set_sdr_rate(self, sdr_rate):
        self.sdr_rate = sdr_rate
        self.set_samp_rate(self.sdr_rate / self.decim)
        self.rtlsdr_source_0.set_sample_rate(self.sdr_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.sdr_rate)

    def get_freqdetectada(self):
        return self.freqdetectada

    def set_freqdetectada(self, freqdetectada):
        self.freqdetectada = freqdetectada
        self.set_variable_qtgui_label_0_2(self._variable_qtgui_label_0_2_formatter(self.freqdetectada))

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_samp_rate(self.sdr_rate / self.decim)

    def get_variable_qtgui_label_0_2(self):
        return self.variable_qtgui_label_0_2

    def set_variable_qtgui_label_0_2(self, variable_qtgui_label_0_2):
        self.variable_qtgui_label_0_2 = variable_qtgui_label_0_2
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_2_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0_2))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)

    def get_fft_n(self):
        return self.fft_n

    def set_fft_n(self, fft_n):
        self.fft_n = fft_n


def main(top_block_cls=garage, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
