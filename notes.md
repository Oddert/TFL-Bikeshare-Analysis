# Notes

## Sweetviz

- Did run: No
- Issues installing with modern packages
- Eventually working with:
  - kagglehub
  - pandas
  - setuptools
  - sweetviz==2.3.1
  - numpy==2.0.1
- Too annoyed to carry on

- Received error:

```console
<frozen importlib._bootstrap>:488: Warning: Numpy built with MINGW-W64 on Windows 64 bits is experimental, and only available for

testing. You are advised not to use it for production.

CRASHES ARE TO BE EXPECTED - PLEASE REPORT THEM TO NUMPY DEVELOPERS
C:\dev\msc-dataeng\bikeshare\venv\Lib\site-packages\numpy\_core\getlimits.py:227: RuntimeWarning: invalid value encountered in exp2
  epsneg_f128 = exp2(ld(-113))
C:\dev\msc-dataeng\bikeshare\venv\Lib\site-packages\numpy\_core\getlimits.py:228: RuntimeWarning: invalid value encountered in exp2
  tiny_f128 = exp2(ld(-16382))
C:\dev\msc-dataeng\bikeshare\venv\Lib\site-packages\numpy\_core\getlimits.py:242: RuntimeWarning: invalid value encountered in exp2
  eps=exp2(ld(-112)),
C:\dev\msc-dataeng\bikeshare\venv\Lib\site-packages\numpy\_core\getlimits.py:41: RuntimeWarning: invalid value encountered in nextafter
  self._smallest_subnormal = nextafter(
C:\dev\msc-dataeng\bikeshare\venv\Lib\site-packages\numpy\_core\getlimits.py:52: RuntimeWarning: invalid value encountered in log10
  self.precision = int(-log10(self.eps))
Segmentation fault
```
