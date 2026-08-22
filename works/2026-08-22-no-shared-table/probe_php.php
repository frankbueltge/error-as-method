<?php
// Session 67 probe runner — PHP / Zend. Same two modes, same conventions as
// probe_python.py: every answer a string, nothing normalised across runtimes.

$SEEDS = json_decode(file_get_contents(__DIR__ . '/seeds.json'), true);

function bits($x) { return bin2hex(pack('E', $x)); }
function unbits($h) { $u = unpack('E', hex2bin($h)); return $u[1]; }
function cps($s) {
    $out = [];
    foreach (mb_str_split($s, 1, 'UTF-8') as $c) $out[] = sprintf('U+%04X', mb_ord($c, 'UTF-8'));
    return implode(' ', $out);
}
// PHP has no strict whole-string numeric conversion; the ordinary one is a cast,
// and it is lenient. Recorded as it is rather than replaced with a strict stand-in.
function numify($s) { return bits((float)$s); }

// The scalar set for L2/L3 -- this runtime's analogue of the classic set.
function scalars() {
    return [['0', 0], ["''", ''], ["'0'", '0'], ['false', false],
            ['none', null], ["'abc'", 'abc'], ['[]', []]];
}

function emit() {
    global $SEEDS;
    $a = [];
    // ---- Family S: answers that descend from the Unicode Character Database ----
    $a['S1']  = cps(mb_strtoupper('ß', 'UTF-8'));
    $a['S2']  = cps(mb_strtoupper('ﬁ', 'UTF-8'));
    $a['S3']  = cps(mb_strtolower('İ', 'UTF-8'));
    $a['S4']  = cps(mb_strtoupper('ı', 'UTF-8'));
    $a['S5']  = cps(mb_strtolower('ΟΔΟΣ', 'UTF-8'));
    $a['S6']  = cps(mb_strtoupper('ᏸ', 'UTF-8'));
    $a['S7']  = cps(mb_strtoupper('ჯ', 'UTF-8'));
    $a['S8']  = cps(mb_strtoupper("\u{10428}", 'UTF-8'));
    $a['S9']  = cps(mb_strtoupper('ǳ', 'UTF-8'));
    $a['S10'] = cps(mb_strtolower('ẞ', 'UTF-8'));

    // ---- Family I: answers written by hand, per runtime ----
    $a['I1']  = (string)(-7 % 3);
    $a['I2']  = (string)(7 % -3);
    $a['I3']  = (string)intdiv(-7, 3);
    $a['I4']  = (string)(0.1 + 0.2);
    $a['I5']  = (string)(1 / 3);
    $a['I6']  = (string)1e21;
    $a['I7']  = (string)(-0.0);
    $r = [];
    foreach ([0.5, 1.5, 2.5, -0.5] as $v) $r[] = (string)round($v);
    $a['I8']  = implode(' ', $r);
    $a['I9']  = ('10' < '9') ? 'true' : 'false';
    $a['I10'] = ('' == 0) ? 'true' : 'false';
    $a['I11'] = (string)strlen("\u{1d11e}");   // PHP strings are byte strings
    $a['I12'] = (0.1 + 0.2 == 0.3) ? 'true' : 'false';
    $s = [10, 9, 1]; sort($s);
    $a['I13'] = implode(' ', $s);
    $a['I14'] = (string)(2 ** 3 ** 2);
    $n = [];
    foreach (['0x10', '010', '1e2', ' 12 '] as $t) $n[] = numify($t);
    $a['I15'] = implode(' ', $n);

    $renderings = [];
    foreach ($SEEDS as $s2) $renderings[$s2['name']] = (string)unbits($s2['bits']);

    $uv = class_exists('IntlChar')
        ? implode('.', array_slice(IntlChar::getUnicodeVersion(), 0, 2)) . ' (intl; mbstring keeps its own tables)'
        : 'not exposed by this runtime';
    return ['runtime' => 'php', 'version' => PHP_VERSION, 'unicode_version' => $uv, 'answers' => $a,
            'checks' => ['L1_roundtrip' => l1(), 'L2_loose_equality' => l2(),
                         'L3_relational_coherence' => l3(), 'L4_division_identity' => l4()],
            'renderings' => $renderings];
}

// L1 -- does this runtime parse back its own default rendering of a double?
function l1() {
    global $SEEDS;
    $detail = [];
    foreach ($SEEDS as $s) {
        $x = unbits($s['bits']);
        $rendered = (string)$x;
        $back = bits((float)$rendered);
        if ($back !== $s['bits'])
            $detail[] = ['seed' => $s['name'], 'rendered' => $rendered, 'back' => $back];
    }
    return ['tested' => count($SEEDS), 'violations' => count($detail), 'detail' => $detail];
}

// L2 -- is this runtime's own equality operator transitive over that set?
function l2() {
    $sc = scalars(); $viol = [];
    foreach ($sc as [$na, $x]) foreach ($sc as [$nb, $y]) foreach ($sc as [$nc, $z])
        if (($x == $y) && ($y == $z) && !($x == $z)) $viol[] = [$na, $nb, $nc];
    return ['operator' => '==', 'set_size' => count($sc),
            'transitivity_violations' => count($viol), 'examples' => array_slice($viol, 0, 5)];
}

// L3 -- if a<=b and a>=b, does this runtime also say a==b?
function l3() {
    $sc = scalars(); $viol = [];
    foreach ($sc as [$na, $x]) foreach ($sc as [$nb, $y])
        if (($x <= $y) && ($x >= $y) && !($x == $y)) $viol[] = [$na, $nb];
    return ['pairs' => count($sc) ** 2, 'incomparable' => 0,
            'violations' => count($viol), 'examples' => array_slice($viol, 0, 5)];
}

// L4 -- does q*b + r == a hold, with this runtime's own intdiv and % ?
function l4() {
    $viol = [];
    foreach ([-13, -8, -7, -1, 0, 1, 7, 8, 13] as $a)
        foreach ([3, -3, 5, -5] as $b) {
            $q = intdiv($a, $b); $r = $a % $b;
            if ($q * $b + $r !== $a) $viol[] = [$a, $b, $q, $r];
        }
    return ['pairs' => 36, 'violations' => count($viol), 'examples' => array_slice($viol, 0, 5)];
}

function parse_mode() {
    $strings = json_decode(stream_get_contents(STDIN), true);
    $out = [];
    foreach ($strings as $s) $out[] = bits((float)$s);
    return $out;
}

$mode = $argv[1] ?? 'emit';
echo json_encode($mode === 'emit' ? emit() : parse_mode()), "\n";
