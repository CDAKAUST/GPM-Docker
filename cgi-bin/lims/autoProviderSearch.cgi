#!/usr/bin/perl -w
use strict;
use CGI qw(:standard);
use CGI::Carp qw ( fatalsToBrowser ); 
use JSON::XS; # imports encode_json, decode_json, to_json and from_json.
use DBI;
use lib "lib/";
use lib "lib/pangu";
use pangu;

my $commoncfg = readParam();
my $htdocs = $commoncfg->getProperty('HTDOCS');
my $dbuser = $commoncfg->getProperty('USERNAME');
my $dbpass = $commoncfg->getProperty('PASSWORD');
my $dbhost = $commoncfg->getProperty('DBHOST');
my $dbdata = $commoncfg->getProperty('DATABASE');

my $dbh=DBI->connect("DBI:mysql:$dbdata:$dbhost",$dbuser,$dbpass);

my $keyword = param("term");
my @results;
print header('application/json');
my $same;
my $sth=$dbh->prepare("SELECT * FROM matrix WHERE container LIKE 'library'");
$sth->execute();
while (my @sth = $sth->fetchrow_array())
{
	my $libraryDetails = decode_json $sth[8];
	if ($libraryDetails->{'providedBy'})
	{
		if (exists $same->{$libraryDetails->{'providedBy'}})
		{
			next;
		}
		else
		{
			if ($libraryDetails->{'providedBy'} =~ /$keyword/i)
			{
				my %hash;
				$hash{'id'} = $libraryDetails->{'providedBy'};
				$hash{'label'} = $libraryDetails->{'providedBy'};
				$hash{'value'} = $libraryDetails->{'providedBy'};
				push @results, \%hash;
			}
			$same->{$libraryDetails->{'providedBy'}} = 1;
		}
	}
}
my $json = JSON::XS->new->allow_nonref;
my $json_text = $json->encode(\@results);
print $json_text;