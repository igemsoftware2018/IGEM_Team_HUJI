###############################################################################
Copyright (C) 2016  Author: Vasileios Rantos
			GNU GENERAL PUBLIC LICENSE
			 Version 3, 29 June 2007
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For further information and support please contact author : vrantos@hotmail.gr
###############################################################################

Author : Vasileios Rantos
Software name : TaiCO
Purpose : tAI based codon optimization of DNA sequences
Special Notes : Nominated for Software Special Award in IGEM 2016, BOSTON,MA 
Team : DTU-DENMARK


1) Description and novelties :

The intention of this file is to provide comprehensive guidelines and information
with regards to what the software that you have donwloaded under the name TaiCO can
offer to the user and how it should be used efficiently.
The TaiCO software is a GUI application implemented in Python, for thorough optimization
of real or not DNA seqs provided the corresponding protein sequences which are being
"back-translated" to DNA and optimized for maximal gene expression.
 
At this point it has to be highlighted that:
a) it is the only computational tool in the world that achieves optimization of DNA
sequences depending on tRNA Adaptation Index (TAI) calculation while providing the
option of eliminating unwanted restriction sites from the resulting sequences
b) downloading of Pythonic libraries and packages and most importantly Python itself
is completely unneccessary due to the usage of PyInstaller software
(http://www.pyinstaller.org/) in order to create the final executable bundle
c) there is a version available at IGEM Software repo at GitHub also for two different OS.

2) Mandatory steps and instructions:

The procedure that you have to follow in order to efficiently use TaiCO was build in
a very structured and simplified way for your convenience and reliable use.

1. Download the version that is applicable for your system (OS) --> 1 zipped file
2. Extract the file (and not be afraid of the bunch of folders and files that will come up)
3. Double click the TaiCO executable (extension dependant on your OS)
4. Click the top "Search file" button to upload a species specific GCN table from the
species folder or you can upload you own file --> BEWARE : KEEP THE SAME FORMAT IN YOUR
FILE AS THE ONES PROVIDED, i.e tab-separated columns (the first two are extremelly important)
and the first anticodon starts from the second line in file 
5. CLick the middle "Search file" button to upload your file with one or multiple queries of
PROTEINS ONLY in FASTA format (please use only amino acids and not special chars like e.g. *)
6. OPTIONAL : Click the bottom last button "Search file" if you want to upload a text file
with a single column of unwanted restriction sites
7. When you are done uploading click the "Start analysis" button and wait for the successful
pop-up message !
8. After the pop-up is closed the resulting file is saved at the same folder where your
executable "lives" under the name optimized_seqs.txt
9. The software is ready to be rerunned without the need of reopening it

Important notes : 
a) If you fail to follow the format instructed above for the files that you upload the analysis
will fail with no error message most of the times and no pop-up successful pop-up.
b) After each run all the files are being cleared from the memory so you have to upload every single
file again following the above isntructions.
c) You are strongly recommended not to move around folders and files in your system becasue
the software will fail finding them again.
d) Depending on the platform the initiation of TaiCO may take some seconds (varying from 2sec - 40sec)

Files provided :
- 7 gcn txt files provided from almost all model organisms in Biology which include:
A. thaliana, M. musculus, S. cerevisiae, Y. lipolytica, E. coli, C. elegans, D. melanogaster

- 1 fasta file with many protein sequences as example for familiarization with TaiCO and 1 txt file with restriction site list as example (all in the folder example_files)

For further information and support please contact author : email: vrantos@hotmail.gr

Also visit our wiki-site for more information regarding the background theory of TaiCO and
read the description for our Yeastilization project presented in IGEM 2016, Boston,MA.
wiki-page : http://2016.igem.org/Team:DTU-Denmark
software tab : http://2016.igem.org/Team:DTU-Denmark/Software


