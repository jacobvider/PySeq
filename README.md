# PySeqX
Automating processes on the Illumina HiSeq X, based on code used for the HiSeq 2500.

**Background:** 
The HiSeq is an instrument used for DNA sequencing. 
It was produced by Illumina, who have recently discontinued this device in favor of newer sequencing technology.
The HiSeq device has a 3-axis motorized stage (x-stage, y-stage, and z-stage), several methods of temperature control including a fluidics system, an integrated fluidics system, and TDI CCD cameras.

**Project Goal:**
PySeqX is an open-source code that controls the HiSeq X device and automates additional HiSeq X applications that go beyond initial sequencing applications. 
PySeq2500 is an open-souce code that already fulfills this purpose for the HiSeq 2500/2000 device, which are predecessors to the HiSeq X device. However, the HiSeq X differs from the HiSeq 2500 in a number of ways, hence the need for updated code.
The HiSeq X has a different driver for the Y stage, a different fluidics system, and a different driver for the CCD camera. 

**PySeq2500 code:**
[Kunal's code](https://github.com/nygctech/PySeq2500/tree/f9445216be3d521b8bdf643b8dd5a73801bec6f3)

[Richard's code](https://github.com/chaichontat/pyseq2501)
