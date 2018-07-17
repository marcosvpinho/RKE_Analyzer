#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: HT12E decoder
# Author: Roberto W. Nobrega
# Generated: Sun Jun 24 15:17:20 2018
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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from ht12e_dec import blk
from optparse import OptionParser
import numpy as np
import wx


class garage(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="HT12E decoder")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.sdr_rate = sdr_rate = 2.88e6
        self.decim = decim = 10
        self.sps = sps = 80
        self.samp_rate = samp_rate = sdr_rate / decim
        self.freq = freq = 299e6

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate,
        	v_scale=0.2,
        	v_offset=0,
        	t_scale=0.2e-3,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=2,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.GridAdd(self.wxgui_scopesink2_0.win, 1, 0, 1, 1)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=True,
        )
        self.GridAdd(self.wxgui_fftsink2_0.win, 2, 0, 1, 1)
        self.ht12e_dec = blk(min_agreements=3, debug=True)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label='freq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=290e6,
        	maximum=310e6,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_freq_sizer, 0, 0, 1, 1)
        self.fir_filter_xxx_1 = filter.fir_filter_ccc(decim, (1, ))
        self.fir_filter_xxx_1.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(1, (np.ones(sps) / (sps)))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(sps, 0.25*0.175*0.175, 0.5, 0.175, 0.1)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, sdr_rate,True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, "/home/marcos/Documentos/TCC/garage/test1_f_2.88M.dat", True)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_const_vxx_2 = blocks.add_const_vff((-0.51, ))
        self.analog_agc_xx_0 = analog.agc_ff(1e-3, 0.333, 1)
        self.analog_agc_xx_0.set_max_gain(1000)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_add_const_vxx_2, 0))    
        self.connect((self.blocks_add_const_vxx_2, 0), (self.fir_filter_xxx_0, 0))    
        self.connect((self.blocks_add_const_vxx_2, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.analog_agc_xx_0, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.fir_filter_xxx_1, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.ht12e_dec, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.fir_filter_xxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.fir_filter_xxx_0, 0), (self.wxgui_scopesink2_0, 1))    
        self.connect((self.fir_filter_xxx_1, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.fir_filter_xxx_1, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.ht12e_dec, 0), (self.blocks_null_sink_0, 0))    

    def get_sdr_rate(self):
        return self.sdr_rate

    def set_sdr_rate(self, sdr_rate):
        self.sdr_rate = sdr_rate
        self.set_samp_rate(self.sdr_rate / self.decim)
        self.blocks_throttle_0.set_sample_rate(self.sdr_rate)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_samp_rate(self.sdr_rate / self.decim)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.digital_clock_recovery_mm_xx_0.set_omega(self.sps)
        self.fir_filter_xxx_0.set_taps((np.ones(self.sps) / (self.sps)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)


def main(top_block_cls=garage, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
