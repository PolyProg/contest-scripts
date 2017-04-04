sudo apt install -y enscript
sudo mkdir /opt/domjudge/print/
sudo chmod 777 /opt/domjudge/print/
sudo mkdir /opt/domjudge/printarchive/
sudo chmod 777 /opt/domjudge/printarchive/

# Patch lib/www/printing in function send_print:
cat << EOF | git apply -
From 0ad6df1655531f3a4aeddd261b84bcbaba9ad9fe Mon Sep 17 00:00:00 2001
From: Solal Pirelli <solal.pirelli@gmail.com>
Date: Wed, 29 Mar 2017 12:05:25 +0200
Subject: [PATCH] POLYPROG: custom printing

---
 lib/www/printing.php | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)

diff --git a/lib/www/printing.php b/lib/www/printing.php
index 6e328a2..3063d99 100644
--- a/lib/www/printing.php
+++ b/lib/www/printing.php
@@ -152,8 +152,8 @@ function send_print($filename, $language = null, $team = null, $origname = null)
 	$cmd = "enscript -C " . $highlight
 	     . " -b " . escapeshellarg($banner)
 	     . " -a 0-10 "
-	// for debugging: uncomment next line
-	//   . " -p /tmp/test.ps "
+	     . " -q "
+	     . " -p /opt/domjudge/print/" . uniqid(rand(), true) . ".ps "
 	     . escapeshellarg($filename) . " 2>&1";

 	exec($cmd, $output, $retval);
--
1.9.1
EOF
