
import unittest
import os
from mplayer_resumer import Player

OUTPUT_BREAK = '''
MPlayer SVN-r35920-4.7.2 (C) 2000-2013 MPlayer Team
203 audio & 421 video codecs

Playing /home/ryan/downloads/test.f4v.
libavformat version 54.63.100 (internal)
libavformat file format detected.
[lavf] stream 0: video (h264), -vid 0
[lavf] stream 1: audio (aac), -aid 0, -alang eng
VIDEO:  [H264]  960x540  24bpp  30.000 fps  1395.4 kbps (170.3 kbyte/s)
Clip info:
 major_brand: mp42
 minor_version: 1
 compatible_brands: isommp41avc1
 creation_time: 2012-05-21 22:38:16
 copyright: lynda.com
 copyright-eng: lynda.com
Load subtitles in /home/ryan/downloads/
Failed to open VDPAU backend libvdpau_nvidia.so: cannot open shared object file: No such file or directory
[vdpau] Error when calling vdp_device_create_x11: 1
[VO_XV] Could not grab port 78.
==========================================================================
Opening video decoder: [ffmpeg] FFmpeg's libavcodec codec family
libavcodec version 54.92.100 (internal)
Selected video codec: [ffh264] vfm: ffmpeg (FFmpeg H.264)
==========================================================================
==========================================================================
Opening audio decoder: [ffmpeg] FFmpeg/libavcodec audio decoders
AUDIO: 48000 Hz, 2 ch, floatle, 128.0 kbit/4.17% (ratio: 15998->384000)
Selected audio codec: [ffaac] afm: ffmpeg (FFmpeg AAC (MPEG-2/MPEG-4 Audio))
==========================================================================
AO: [alsa] 48000Hz 2ch floatle (4 bytes per sample)
Starting playback...
Movie-Aspect is 1.78:1 - prescaling to correct movie aspect.
VO: [xv] 960x540 => 960x540 Planar YV12
A:   0.6 V:   1.0 A-V:  0.000 ct:  0.000   0/  0 31%  5%  0.6% 2 0
A:   0.7 V:   1.0 A-V:  0.000 ct:  0.000   0/  0 31%  5%  0.6% 2 0
A:   0.9 V:   1.0 A-V:  0.000 ct:  0.000   0/  0 31%  5%  0.6% 2 0
A:   1.0 V:   1.0 A-V:  0.000 ct:  0.000   0/  0 31%  5%  0.6% 2 0

Exiting... (Quit)
'''

OUTPUT_COMPLETE = '''
MPlayer SVN-r35920-4.7.2 (C) 2000-2013 MPlayer Team
203 audio & 421 video codecs

Playing /home/ryan/downloads/test.f4v.
libavformat version 54.63.100 (internal)
libavformat file format detected.
[lavf] stream 0: video (h264), -vid 0
[lavf] stream 1: audio (aac), -aid 0, -alang eng
VIDEO:  [H264]  960x540  24bpp  30.000 fps  1395.4 kbps (170.3 kbyte/s)
Clip info:
 major_brand: mp42
 minor_version: 1
 compatible_brands: isommp41avc1
 creation_time: 2012-05-21 22:38:16
 copyright: lynda.com
 copyright-eng: lynda.com
Load subtitles in /home/ryan/downloads/
Failed to open VDPAU backend libvdpau_nvidia.so: cannot open shared object file: No such file or directory
[vdpau] Error when calling vdp_device_create_x11: 1
[VO_XV] Could not grab port 78.
==========================================================================
Opening video decoder: [ffmpeg] FFmpeg's libavcodec codec family
libavcodec version 54.92.100 (internal)
Selected video codec: [ffh264] vfm: ffmpeg (FFmpeg H.264)
==========================================================================
==========================================================================
Opening audio decoder: [ffmpeg] FFmpeg/libavcodec audio decoders
AUDIO: 48000 Hz, 2 ch, floatle, 128.0 kbit/4.17% (ratio: 15998->384000)
Selected audio codec: [ffaac] afm: ffmpeg (FFmpeg AAC (MPEG-2/MPEG-4 Audio))
==========================================================================
AO: [alsa] 48000Hz 2ch floatle (4 bytes per sample)
Starting playback...
Movie-Aspect is 1.78:1 - prescaling to correct movie aspect.
VO: [xv] 960x540 => 960x540 Planar YV12
A:  55.2 V:  85.2 A-V: -0.016 ct: -0.014   0/  0  9%  1%  0.4% 0 0
A:  65.2 V:  85.2 A-V: -0.016 ct: -0.014   0/  0  9%  1%  0.4% 0 0
A:  75.2 V:  85.2 A-V: -0.016 ct: -0.014   0/  0  9%  1%  0.4% 0 0
A:  85.2 V:  85.2 A-V: -0.016 ct: -0.014   0/  0  9%  1%  0.4% 0 0


Exiting... (End of file)
'''


class MainTest(unittest.TestCase):

    def setUp(self):
        self.movie = "/media/Resources/Videos/python/Lynda.com.Foundations.of.\
                Programming.Object-Oriented.Design/00.\ Introduction/00\ 01.\ Welcome.f4v"
        self.player = Player(self.movie)

    def test_get_file_abspath(self):
        self.assertEqual(self.player.get_file_abspath(self.movie), self.movie)
        self.assertEqual(self.player.get_file_abspath("__init__.py"),
                         "/home/ryan/local/scripts/python/mplayer_resumer/__init__.py")
    def test_amend_break_time(self):
        self.assertEqual(self.player.amend_break_time(3), "3.0")
        self.assertEqual(self.player.amend_break_time(12), "7.0")

    def test_parse_break_time(self):
        self.assertEqual(self.player.parse_break_time(OUTPUT_BREAK), "1.0")
        self.assertEqual(self.player.parse_break_time(OUTPUT_COMPLETE), "85.2")

    def test_parse_stop_status(self):
        self.assertTrue(self.player.parse_stop_status(OUTPUT_BREAK))
        self.assertFalse(self.player.parse_stop_status(OUTPUT_COMPLETE))

if __name__ == "__main__":
    unittest.main()
