#!/usr/bin/env perl
# Session 67 probe runner — perl5. Same two modes, same conventions as
# probe_python.py: every answer a string, nothing normalised across runtimes.
#
# Perl is the one runtime here that splits operators other languages fuse:
# numeric == against string eq, numeric < against string lt. Where that
# happens the answer names both rather than picking one silently.
use strict;
use warnings;
use utf8;
use FindBin;
use JSON::PP;
use POSIX ();
use Config;

my $J = JSON::PP->new->canonical->allow_nonref;
my $SEEDS = $J->decode(do { local (@ARGV, $/) = ("$FindBin::Bin/seeds.json"); <> });

sub bits   { return unpack('H*', pack('d>', $_[0])); }
sub unbits { return unpack('d>', pack('H*', $_[0])); }
sub cps    { return join(' ', map { sprintf('U+%04X', ord($_)) } split //, $_[0]); }
# Perl has no strict whole-string numeric conversion; the ordinary one is
# numeric context, and it is lenient. Recorded as it is.
sub numify { no warnings 'numeric'; return bits(0 + $_[0]); }

# The scalar set for L2/L3. Note what is already visible in the list: Perl's
# false and its empty string are the SAME scalar, so the classic seven-element
# set has only six distinct members here.
sub scalars {
    return (['0', 0], ["''", ''], ["'0'", '0'], ['false', !!0],
            ['none', undef], ["'abc'", 'abc'], ['[]', []]);
}

sub emit {
    my %a;
    # ---- Family S: answers that descend from the Unicode Character Database ----
    $a{S1}  = cps(uc('ß'));
    $a{S2}  = cps(uc('ﬁ'));
    $a{S3}  = cps(lc('İ'));
    $a{S4}  = cps(uc('ı'));
    $a{S5}  = cps(lc('ΟΔΟΣ'));
    $a{S6}  = cps(uc('ᏸ'));
    $a{S7}  = cps(uc('ჯ'));
    $a{S8}  = cps(uc("\x{10428}"));
    $a{S9}  = cps(uc('ǳ'));
    $a{S10} = cps(lc('ẞ'));

    # ---- Family I: answers written by hand, per runtime ----
    $a{I1}  = '' . (-7 % 3);
    $a{I2}  = '' . (7 % -3);
    $a{I3}  = 'n/a: no integer division operator (int(-7/3) gives: ' . int(-7 / 3) . ')';
    $a{I4}  = '' . (0.1 + 0.2);
    $a{I5}  = '' . (1 / 3);
    $a{I6}  = '' . 1e21;
    $a{I7}  = '' . (-0.0);
    $a{I8}  = 'n/a: no round builtin (sprintf "%.0f" gives: '
            . join(' ', map { sprintf('%.0f', $_) } (0.5, 1.5, 2.5, -0.5)) . ')';
    $a{I9}  = (('10' lt '9') ? 'true' : 'false') . ' (lt); '
            . ((0 + '10' < 0 + '9') ? 'true' : 'false') . ' (numeric <)';
    { no warnings 'numeric';
      $a{I10} = (('' == 0) ? 'true' : 'false') . ' (numeric ==); '
              . (('' eq 0) ? 'true' : 'false') . ' (string eq)'; }
    $a{I11} = '' . length("\x{1d11e}");
    $a{I12} = ((0.1 + 0.2 == 0.3) ? 'true' : 'false');
    $a{I13} = join(' ', sort (10, 9, 1));
    $a{I14} = '' . (2**3**2);
    $a{I15} = join(' ', map { numify($_) } ('0x10', '010', '1e2', ' 12 '));

    my %renderings = map { $_->{name} => '' . unbits($_->{bits}) } @$SEEDS;

    my $uv = 'not exposed by this runtime';
    if (open my $vf, '<', "$Config{privlib}/unicore/version") { chomp($uv = <$vf>); }
    return { runtime => 'perl', version => sprintf('%vd', $^V), unicode_version => $uv, answers => \%a,
             checks => { L1_roundtrip => l1(), L2_loose_equality => l2(),
                         L3_relational_coherence => l3(), L4_division_identity => l4() },
             renderings => \%renderings };
}

# L1 -- does this runtime parse back its own default rendering of a double?
sub l1 {
    my @detail;
    for my $s (@$SEEDS) {
        my $x = unbits($s->{bits});
        my $rendered = '' . $x;
        no warnings 'numeric';
        # numify a COPY: numeric context on $rendered itself would add a numeric
        # flag to the scalar and make it serialise as a number rather than a string
        my $copy = $rendered;
        my $back = bits(0 + $copy);
        push @detail, { seed => $s->{name}, rendered => $rendered, back => $back }
            if $back ne $s->{bits};
    }
    return { tested => scalar(@$SEEDS), violations => scalar(@detail), detail => \@detail };
}

# L2 -- transitivity, run separately for each of Perl's two equality operators.
sub l2 {
    my @sc = scalars();
    my %out;
    for my $op ('==', 'eq') {
        my @viol;
        no warnings;
        for my $A (@sc) { for my $B (@sc) { for my $C (@sc) {
            my ($x, $y, $z) = ($A->[1], $B->[1], $C->[1]);
            my ($ab, $bc, $ac) = $op eq '=='
                ? (($x == $y), ($y == $z), ($x == $z))
                : (($x eq $y), ($y eq $z), ($x eq $z));
            push @viol, [$A->[0], $B->[0], $C->[0]] if $ab && $bc && !$ac;
        }}}
        $out{$op} = { transitivity_violations => scalar(@viol),
                      examples => [@viol[0 .. ($#viol > 4 ? 4 : $#viol)]] };
    }
    return { operator => 'two operators: == and eq', set_size => scalar(@sc),
             transitivity_violations => $out{'=='}{transitivity_violations}
                                      + $out{'eq'}{transitivity_violations},
             per_operator => \%out,
             examples => [@{ $out{'=='}{examples} }, @{ $out{'eq'}{examples} }] };
}

# L3 -- if a<=b and a>=b, does this runtime also say a==b? Numeric operators.
sub l3 {
    my @sc = scalars();
    my @viol;
    no warnings;
    for my $A (@sc) { for my $B (@sc) {
        my ($x, $y) = ($A->[1], $B->[1]);
        push @viol, [$A->[0], $B->[0]] if ($x <= $y) && ($x >= $y) && !($x == $y);
    }}
    return { pairs => scalar(@sc) ** 2, incomparable => 0,
             violations => scalar(@viol), examples => [@viol[0 .. ($#viol > 4 ? 4 : $#viol)]] };
}

# L4 -- does q*b + r == a hold? Perl has no integer-division operator, so the
# pairing is not given by the language and BOTH candidate pairings are reported.
sub l4 {
    my (@viol_trunc, @viol_floor);
    for my $a (-13, -8, -7, -1, 0, 1, 7, 8, 13) {
        for my $b (3, -3, 5, -5) {
            my $r  = $a % $b;
            my $qt = int($a / $b);            # truncating: Perl's int()
            my $qf = POSIX::floor($a / $b);   # flooring
            push @viol_trunc, [$a, $b, $qt, $r] if $qt * $b + $r != $a;
            push @viol_floor, [$a, $b, $qf, $r] if $qf * $b + $r != $a;
        }
    }
    return { pairs => 36,
             violations => scalar(@viol_trunc),
             note => 'no integer-division operator; two pairings reported',
             with_int_truncating => { violations => scalar(@viol_trunc),
                                      examples => [@viol_trunc[0 .. ($#viol_trunc > 4 ? 4 : $#viol_trunc)]] },
             with_floor         => { violations => scalar(@viol_floor),
                                      examples => [@viol_floor[0 .. ($#viol_floor > 4 ? 4 : $#viol_floor)]] },
             examples => [@viol_trunc[0 .. ($#viol_trunc > 4 ? 4 : $#viol_trunc)]] };
}

sub parse_mode {
    my $in = do { local $/; <STDIN> };
    my $strings = $J->decode($in);
    no warnings 'numeric';
    return [map { bits(0 + $_) } @$strings];
}

my $mode = $ARGV[0] // 'emit';
print $J->encode($mode eq 'emit' ? emit() : parse_mode()), "\n";
