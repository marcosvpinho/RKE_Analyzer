#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: RKE Analyzer
# Author: Marcos
# Generated: Tue Feb 12 16:38:46 2019
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
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import crossing
import detectorx
import divide
import insert_tag
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
        self.sps1 = sps1 = 1
        self.sdr_rate = sdr_rate = 2e6
        self.my_seq = my_seq = 0
        self.my_encoder = my_encoder = 0
        self.freqdetectada = freqdetectada = 292e6
        self.decim = decim = 20
        self.variable_qtgui_label_0_2 = variable_qtgui_label_0_2 = freqdetectada
        self.variable_qtgui_label_0_1_0 = variable_qtgui_label_0_1_0 = my_seq
        self.variable_qtgui_label_0_1 = variable_qtgui_label_0_1 = my_encoder
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0 = sps1
        self.sps = sps = 44
        self.samp_rate = samp_rate = sdr_rate / decim
        self.gain = gain = 0.01
        self.freq_list = freq_list = (292000000, 299000000, 315000000, 434000000)
        self.freq = freq = 0
        self.fft_n = fft_n = 2048
        self.encoder_length = encoder_length = ((12,"HT12E - M1E-N"),(28,"HT6P20B"),(9,"HT6026 - MC145026"))
        self.encoder_code = encoder_code = ((([((0,0,0,0,0,0,0,1), 'P'), ((0,1,1), 0), ((0,0,1), 1)])),(([((0,0,0,0,0,0,0,1), 'P'), ((0,1,1), 0), ((0,0,1), 1)])),(([((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 'P'),((0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1), 1),((0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0), 0),((0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0), "Z")])))

        ##################################################
        # Blocks
        ##################################################
        self.sumx = sumx.summ(limiar_db=25, freq_list=freq_list, sample_rate=sdr_rate, len_fft=fft_n)
        self.crossing = crossing.crossing(sample_rate=samp_rate, threshold=10)

        def _sps_probe():
            while True:
                val = self.crossing.retorna_sps()
                try:
                    self.set_sps(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (5))
        _sps_thread = threading.Thread(target=_sps_probe)
        _sps_thread.daemon = True
        _sps_thread.start()


        def _freqdetectada_probe():
            while True:
                val = self.sumx.freq_detectada()
                try:
                    self.set_freqdetectada(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (5))
        _freqdetectada_thread = threading.Thread(target=_freqdetectada_probe)
        _freqdetectada_thread.daemon = True
        _freqdetectada_thread.start()


        def _freq_probe():
            while True:
                val = self.sumx.freq_ativa()
                try:
                    self.set_freq(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (5))
        _freq_thread = threading.Thread(target=_freq_probe)
        _freq_thread.daemon = True
        _freq_thread.start()

        self.detectorx = detectorx.blkfinal(decoders_list=encoder_code, decoders_length=encoder_length)
        self._variable_qtgui_label_0_2_tool_bar = Qt.QToolBar(self)

        if None:
          self._variable_qtgui_label_0_2_formatter = None
        else:
          self._variable_qtgui_label_0_2_formatter = lambda x: eng_notation.num_to_str(x)

        self._variable_qtgui_label_0_2_tool_bar.addWidget(Qt.QLabel('Frequencia Detectada'+": "))
        self._variable_qtgui_label_0_2_label = Qt.QLabel(str(self._variable_qtgui_label_0_2_formatter(self.variable_qtgui_label_0_2)))
        self._variable_qtgui_label_0_2_tool_bar.addWidget(self._variable_qtgui_label_0_2_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_2_tool_bar)
        self._variable_qtgui_label_0_1_0_tool_bar = Qt.QToolBar(self)

        if None:
          self._variable_qtgui_label_0_1_0_formatter = None
        else:
          self._variable_qtgui_label_0_1_0_formatter = lambda x: repr(x)

        self._variable_qtgui_label_0_1_0_tool_bar.addWidget(Qt.QLabel('Quadro'+": "))
        self._variable_qtgui_label_0_1_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_1_0_formatter(self.variable_qtgui_label_0_1_0)))
        self._variable_qtgui_label_0_1_0_tool_bar.addWidget(self._variable_qtgui_label_0_1_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_1_0_tool_bar)
        self._variable_qtgui_label_0_1_tool_bar = Qt.QToolBar(self)

        if None:
          self._variable_qtgui_label_0_1_formatter = None
        else:
          self._variable_qtgui_label_0_1_formatter = lambda x: repr(x)

        self._variable_qtgui_label_0_1_tool_bar.addWidget(Qt.QLabel('Codificador'+": "))
        self._variable_qtgui_label_0_1_label = Qt.QLabel(str(self._variable_qtgui_label_0_1_formatter(self.variable_qtgui_label_0_1)))
        self._variable_qtgui_label_0_1_tool_bar.addWidget(self._variable_qtgui_label_0_1_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_1_tool_bar)
        self._variable_qtgui_label_0_0_tool_bar = Qt.QToolBar(self)

        if None:
          self._variable_qtgui_label_0_0_formatter = None
        else:
          self._variable_qtgui_label_0_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_0_tool_bar.addWidget(Qt.QLabel('Frequencia do clock'+": "))
        self._variable_qtgui_label_0_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_0_formatter(self.variable_qtgui_label_0_0)))
        self._variable_qtgui_label_0_0_tool_bar.addWidget(self._variable_qtgui_label_0_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_0_tool_bar)

        def _sps1_probe():
            while True:
                val = self.crossing.retorna_freq()
                try:
                    self.set_sps1(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _sps1_thread = threading.Thread(target=_sps1_probe)
        _sps1_thread.daemon = True
        _sps1_thread.start()

        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(sdr_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(20, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
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

        if not False:
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
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.probe = blocks.probe_signal_i()

        def _my_seq_probe():
            while True:
                val = self.detectorx.retorna_sequencia_detectada()
                try:
                    self.set_my_seq(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _my_seq_thread = threading.Thread(target=_my_seq_probe)
        _my_seq_thread.daemon = True
        _my_seq_thread.start()


        def _my_encoder_probe():
            while True:
                val = self.detectorx.retorna_codificador_detectado()
                try:
                    self.set_my_encoder(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _my_encoder_thread = threading.Thread(target=_my_encoder_probe)
        _my_encoder_thread.daemon = True
        _my_encoder_thread.start()

        self.insert_tag = insert_tag.clock_reset(sps=sps)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decim, (1, ), freqdetectada - freq, sdr_rate)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(1, (np.ones(sps) / (sps)))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.fft = fft.fft_vcc(fft_n, True, (window.blackmanharris(fft_n)), True, 1)
        self.divide = divide.divide(threshold=0.1)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(digital.TED_ZERO_CROSSING, 40, 0.1, 1.0, gain, 35, 1, digital.constellation_bpsk().base(), digital.IR_MMSE_8TAP, 128, ([]))
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_n)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_float_to_int_0 = blocks.float_to_int(1, 1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_n)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.divide, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.sumx, 0))
        self.connect((self.blocks_float_to_int_0, 0), (self.probe, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.detectorx, 0))
        self.connect((self.digital_symbol_sync_xx_0, 3), (self.blocks_float_to_int_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 2), (self.blocks_null_sink_0, 1))
        self.connect((self.digital_symbol_sync_xx_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.divide, 0), (self.crossing, 0))
        self.connect((self.divide, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.fft, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.insert_tag, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.insert_tag, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "garage")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps1(self):
        return self.sps1

    def set_sps1(self, sps1):
        self.sps1 = sps1
        self.set_variable_qtgui_label_0_0(self._variable_qtgui_label_0_0_formatter(self.sps1))

    def get_sdr_rate(self):
        return self.sdr_rate

    def set_sdr_rate(self, sdr_rate):
        self.sdr_rate = sdr_rate
        self.set_samp_rate(self.sdr_rate / self.decim)
        self.sumx.sample_rate = self.sdr_rate
        self.rtlsdr_source_0.set_sample_rate(self.sdr_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.sdr_rate)

    def get_my_seq(self):
        return self.my_seq

    def set_my_seq(self, my_seq):
        self.my_seq = my_seq
        self.set_variable_qtgui_label_0_1_0(self._variable_qtgui_label_0_1_0_formatter(self.my_seq))

    def get_my_encoder(self):
        return self.my_encoder

    def set_my_encoder(self, my_encoder):
        self.my_encoder = my_encoder
        self.set_variable_qtgui_label_0_1(self._variable_qtgui_label_0_1_formatter(self.my_encoder))

    def get_freqdetectada(self):
        return self.freqdetectada

    def set_freqdetectada(self, freqdetectada):
        self.freqdetectada = freqdetectada
        self.set_variable_qtgui_label_0_2(self._variable_qtgui_label_0_2_formatter(self.freqdetectada))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.freqdetectada - self.freq)

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

    def get_variable_qtgui_label_0_1_0(self):
        return self.variable_qtgui_label_0_1_0

    def set_variable_qtgui_label_0_1_0(self, variable_qtgui_label_0_1_0):
        self.variable_qtgui_label_0_1_0 = variable_qtgui_label_0_1_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_1_0_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0_1_0))

    def get_variable_qtgui_label_0_1(self):
        return self.variable_qtgui_label_0_1

    def set_variable_qtgui_label_0_1(self, variable_qtgui_label_0_1):
        self.variable_qtgui_label_0_1 = variable_qtgui_label_0_1
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_1_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0_1))

    def get_variable_qtgui_label_0_0(self):
        return self.variable_qtgui_label_0_0

    def set_variable_qtgui_label_0_0(self, variable_qtgui_label_0_0):
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_0_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0_0))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.insert_tag.sps = self.sps
        self.fir_filter_xxx_0.set_taps((np.ones(self.sps) / (self.sps)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.digital_symbol_sync_xx_0.set_ted_gain(self.gain)

    def get_freq_list(self):
        return self.freq_list

    def set_freq_list(self, freq_list):
        self.freq_list = freq_list

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.freqdetectada - self.freq)

    def get_fft_n(self):
        return self.fft_n

    def set_fft_n(self, fft_n):
        self.fft_n = fft_n
        self.sumx.len_fft = self.fft_n

    def get_encoder_length(self):
        return self.encoder_length

    def set_encoder_length(self, encoder_length):
        self.encoder_length = encoder_length

    def get_encoder_code(self):
        return self.encoder_code

    def set_encoder_code(self, encoder_code):
        self.encoder_code = encoder_code


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
