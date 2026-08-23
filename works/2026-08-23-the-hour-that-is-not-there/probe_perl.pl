#!/usr/bin/perl
# Perl probe. Reads a job on stdin, answers on stdout, in its own words.
#
# PRODUCER ONLY. Perl core ships no general-purpose date-time parser: Date::Parse, HTTP::Date
# and DateTime are all absent from this installation, and core Time::Piece->strptime requires a
# format string the caller supplies. Any lenient Perl parser in this work would be MINE, and its
# failures would be mine, not Perl's -- which is exactly the attribution error Session 67 filed
# as C1 and the third of three consecutive nights. So this probe renders and does not parse.
#
# Rendering:
#   default -- scalar(localtime($e)). perlfunc: "in scalar context, localtime() returns
#              [...] a string" of the form "Thu Oct 13 04:54:34 1994". No offset, no zone name.
#   iso     -- POSIX::strftime with "%Y-%m-%dT%H:%M:%S%z" over localtime.
# Numbers:
#   $s + 0 -- Perl's implicit string-to-number coercion, under no warnings so that the value
#             rather than the diagnostic is what gets recorded.

use strict;
use warnings;
use JSON::PP;
use POSIX qw(strftime);

my $raw = do { local $/; <STDIN> };
my $job = decode_json($raw);
my %out = (runtime => 'perl', version => sprintf('%vd', $^V));

if ($job->{instants}) {
    my @r;
    for my $e (@{ $job->{instants} }) {
        my %row = (default => undef, default_error => undef,
                   iso => undef, iso_error => undef);
        my @lt = eval { localtime($e) };
        if ($@ || !@lt) {
            $row{default_error} = "localtime failed: $@";
            $row{iso_error}     = $row{default_error};
        } else {
            $row{default} = eval { scalar localtime($e) };
            $row{default_error} = "$@" if $@;
            $row{iso} = eval { strftime('%Y-%m-%dT%H:%M:%S%z', localtime($e)) };
            $row{iso_error} = "$@" if $@;
        }
        push @r, \%row;
    }
    $out{render} = \@r;
}

# No 'parse' key is ever emitted. See the note at the top.
$out{parse_absent} = JSON::PP::true;
$out{parse_absent_reason} =
    'Perl core ships no general-purpose date-time parser in this installation '
  . '(Date::Parse, HTTP::Date, DateTime all missing; Time::Piece->strptime needs a caller-supplied '
  . 'format). A parser written here would be the harness, not the runtime.';

if ($job->{numbers}) {
    my @r;
    for my $s (@{ $job->{numbers} }) {
        no warnings;
        my $v = $s + 0;
        my $enc = ($v == $v && $v != 9**9**9 && $v != -9**9**9) ? $v + 0 : "$v";
        push @r, { lenient => $enc, strict => undef, strict_absent => JSON::PP::true };
    }
    $out{numparse} = \@r;
}

print JSON::PP->new->canonical->encode(\%out);
