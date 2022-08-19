#! /usr/bin/perl

$inf = "infile.txt";

@GlacierList = ();

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
    #copy successful convert it
    
  }
  elsif($stat == 2)
  {
    push(@GlacierList,$mov);
    #print(@GlacierList);
  }
  print("\n==========\n");

}
close(INF);
