<?php

echo "Python Test001 ";

exec("python zte.py",$output,$exitcode);

echo $exitcode;
print_r ($output);
echo '\n';

exec("ping 10.238.151.50&",$output,$exitcode);
echo $exitcode;
print_r ($output);
echo '\n';

?>
