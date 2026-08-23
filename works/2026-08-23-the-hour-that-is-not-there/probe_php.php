<?php
// PHP probe. Reads a job on stdin, answers on stdout, in its own words.
//
// Rendering:
//   default -- the 'date' property PHP itself materialises when a DateTime is cast to an array
//              or serialised: format 'Y-m-d H:i:s.u', with no offset. PHP has no __toString on
//              DateTime, so this is the nearest thing to a default the language supplies of its
//              own accord rather than at a caller's instruction. Recorded as such, not as "the"
//              default; DATE_ATOM is measured separately as the explicit form.
//   iso     -- format(DATE_ATOM), the constant PHP ships for ISO-8601/RFC 3339.
// Parsing:
//   new DateTime($s), which routes through PHP's own date/time parser.
// Numbers:
//   (float)$s -- PHP's implicit string-to-number coercion, which does not raise.
//   And a strict companion via filter_var(..., FILTER_VALIDATE_FLOAT).

$job = json_decode(stream_get_contents(STDIN), true);
$out = array('runtime' => 'php', 'version' => PHP_VERSION,
             'default_timezone' => date_default_timezone_get(),
             'TZ_env' => getenv('TZ') === false ? null : getenv('TZ'));

if (isset($job['instants'])) {
    $r = array();
    foreach ($job['instants'] as $e) {
        $row = array('default' => null, 'default_error' => null,
                     'iso' => null, 'iso_error' => null);
        try {
            $d = new DateTime('@' . $e);
            $d->setTimezone(new DateTimeZone(date_default_timezone_get()));
            $arr = (array) $d;
            $row['default'] = isset($arr['date']) ? $arr['date'] : null;
            $row['iso'] = $d->format(DATE_ATOM);
        } catch (Throwable $ex) {
            $row['default_error'] = get_class($ex) . ': ' . $ex->getMessage();
            $row['iso_error'] = $row['default_error'];
        }
        $r[] = $row;
    }
    $out['render'] = $r;
}

if (isset($job['strings'])) {
    $r = array();
    foreach ($job['strings'] as $s) {
        try {
            $d = new DateTime($s);
            $r[] = array('status' => 'ok', 'epoch' => (float) $d->format('U.u'));
        } catch (Throwable $ex) {
            $r[] = array('status' => 'refused',
                         'error' => get_class($ex) . ': ' . $ex->getMessage());
        }
    }
    $out['parse'] = $r;
}

if (isset($job['numbers'])) {
    $r = array();
    foreach ($job['numbers'] as $s) {
        $lenient = (float) $s;
        $strict = filter_var($s, FILTER_VALIDATE_FLOAT);
        $enc = function ($x) { return is_finite($x) ? $x : (string) $x; };
        $r[] = array('lenient' => $enc($lenient),
                     'strict' => ($strict === false ? null : $enc($strict)),
                     'strict_error' => ($strict === false ? 'FILTER_VALIDATE_FLOAT' : null));
    }
    $out['numparse'] = $r;
}

echo json_encode($out);
