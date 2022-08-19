#! /usr/bin/perl


#Pattern of the bad
#silence_end: 2548.6 | silence_duration: 2548.6

#commands:
#/Users/ronnieperez/Downloads/zdel/scripts/ffmpeg -i zbad.mp3 -af "pan=1c|c0=c0,silencedetect=noise=-18dB:d=0.5" -f null -
#/Users/ronnieperez/Downloads/zdel/scripts/ffmpeg -i zbad.mp3 -af "pan=1c|c0=c1,silencedetect=noise=-18dB:d=0.5" -f null -

$movf = shift(@ARGV);

foreach $n (0..1)
{
  $cmd = "./ffmpeg -i $movf -af \"pan=1c|c0=c$n,silencedetect=noise=-18dB:d=0.5\" -f null -";
  #print("$cmd\n");
}
