#! /usr/bin/perl

$inf  = "infile.txt";
$outf = "log.txt";

@GlacierList = ();

unless (open OUTF, ">$outf")
{
  print("Cannot open output file $outf\n");
  exit(1);
}

sub getMOV
{

  $mov = "\"$_[0]\"";
  $cmd = "aws s3 cp $mov .";
  print("  ~~$cmd~~\n");

  unless (open CMD, "$cmd |")
  {
    print("Cannot run command $cmd\n");
    exit(1);
  }

  while(<CMD>)
  {
    chomp;
    print("$_\n");
  }
  close(CMD);

  $exitstat = $? >> 8;
  return $exitstat;
}


sub getMP3
{
  $f = $_[0];
  $cmd = "./convertmov.py $f";

  print("  ~~$cmd~~\n");

  unless (open CMD, "$cmd |")
  {
    print("Cannot run command $cmd\n");
    exit(1);
  }

  while(<CMD>)
  {
    chomp;
    print("$_\n");
  }
  close(CMD);

  $exitstat = $? >> 8;
  return $exitstat;

}



unless (open INF, "<$inf")
{
  print("  ~~Cannot open input file $inf\n");
  exit(1);
}

while(<INF>)
{
  chomp;

  $mov = $_;
  $stat = &getMOV($mov);

  if ($stat == 0)
  {

    @parts = split/\//,$mov;
    $movf  = pop(@parts);
    $movf  =~ s/"//;
    #print("$movf\n");

    $exstat = &getMP3($movf);

    if ($exstat == 0)
    {
      system("rm $mov");
      print OUTF ("$mov : CONVERTED\n");
    }


  }
  elsif($stat == 2)
  {
    push(@GlacierList,$mov);
    print OUTF ("$mov : GLACIER\n");
  }
  else
  {
    print OUTF ("$mov : ERROR\n");
  }
  print("\n==========\n");

}
close(INF);
close(OUTF);
