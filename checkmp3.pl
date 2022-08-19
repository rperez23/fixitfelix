#! /usr/bin/perl




#commands:
#/Users/ronnieperez/Downloads/zdel/scripts/ffmpeg -i zbad.mp3 -af "pan=1c|c0=c0,silencedetect=noise=-18dB:d=0.5" -f null -
#/Users/ronnieperez/Downloads/zdel/scripts/ffmpeg -i zbad.mp3 -af "pan=1c|c0=c1,silencedetect=noise=-18dB:d=0.5" -f null -


$movf = shift(@ARGV);
$inf  = "audio.txt.$$";

foreach $n (reverse 0..1)
{
  
  $cmd = "./ffmpeg -i $movf -af \"pan=1c|c0=c$n,silencedetect=noise=-18dB:d=0.5\" -f null - > $inf 2>&1";
  `$cmd`;

  unless (open INF, "<$inf")
  {
    print("  ~~Cannot open input file $inf~~\n");
    exit(1);
  }

  while(<INF>)
  {
    chomp;

    #Pattern of the bad
    #silence_end: 2548.6 | silence_duration: 2548.6

    #if (/silence_end: ([0-9\.]+) \| silence_duration: ([0-9\.]+)/)
    if (/silence_end: ([0-9]{4})\.\d+ \| silence_duration: ([0-9]{4})\.\d+/)

    {
      if ($1 == $2)
      {
        print("$movf : MUTED AUDIO POSSIBLE\n");
        `rm $inf`;
        close(INF);
        exit(0);

        #print("  $cmd\n");
        #print("  $_\n");
      }
    }
  }
  close(INF);

  `rm $inf`;

}
