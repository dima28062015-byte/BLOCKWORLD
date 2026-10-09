import os, zipfile, textwrap, shutil

root="/mnt/data/BLOCKWORLD_Android"
if os.path.exists(root):
    shutil.rmtree(root)
os.makedirs(root+"/app/src/main/assets", exist_ok=True)
os.makedirs(root+"/app/src/main/java/com/blockworld/game", exist_ok=True)
os.makedirs(root+"/app/src/main/res/layout", exist_ok=True)
os.makedirs(root+"/app/src/main/res/mipmap-hdpi", exist_ok=True)

files = {
"settings.gradle": """pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }
rootProject.name = "BLOCKWORLD"
include(":app")
""",
"build.gradle": """plugins {
    id 'com.android.application' version '8.7.3' apply false
}
""",
"app/build.gradle": """plugins { id 'com.android.application' }

android { namespace 'com.blockworld.game'; compileSdk 35
    defaultConfig { applicationId 'com.blockworld.game'; minSdk 23; targetSdk 35; versionCode 1; versionName '1.0' }
}
""",
"app/src/main/AndroidManifest.xml": """<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <application android:theme="@style/AppTheme" android:label="BLOCKWORLD" android:resizeableActivity="true">
        <activity android:name=".MainActivity" android:screenOrientation="unspecified" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
""",
"app/src/main/res/values/styles.xml": """<resources>
<style name="AppTheme" parent="android:style/Theme.Material.Light.NoActionBar">
    <item name="android:fontFamily">sans</item>
    <item name="android:windowFullscreen">true</item>
    <item name="android:colorAccent">#00AEEF</item>
</style>
</resources>
""",
"app/src/main/java/com/blockworld/game/MainActivity.java": """package com.blockworld.game;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    @Override public void onCreate(Bundle b) {
        super.onCreate(b);
        WebView w = new WebView(this);
        w.setWebViewClient(new WebViewClient());
        WebSettings s = w.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        w.loadUrl("file:///android_asset/index.html");
        setContentView(w);
    }
}
""",
"app/src/main/assets/index.html": """<!doctype html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>BLOCKWORLD</title>
<style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#79c8ff;font-family:Arial;color:white}
#menu{position:absolute;inset:0;background:linear-gradient(#58b7ff,#bcecff);display:flex;flex-direction:column;align-items:center;justify-content:center}
h1{font-size:48px;margin:0 0 30px;text-shadow:3px 3px #3979a8}
button{font-size:22px;padding:16px 34px;margin:8px;border:0;border-radius:14px;background:#fff;color:#222;font-weight:bold}
#game{display:none;position:absolute;inset:0}
#world{width:100%;height:100%;background:linear-gradient(#72c8ff 0 60%,#68b94c 60%);position:relative}
#player{position:absolute;left:50%;top:55%;width:38px;height:55px;background:#f5c542;border-radius:10px;transform:translate(-50%,-50%)}
#hint{position:absolute;top:15px;left:15px;background:#0008;padding:10px;border-radius:10px}
#joy{position:absolute;bottom:25px;left:25px;width:110px;height:110px;border:3px solid #fff8;border-radius:50%}
#look{position:absolute;right:0;bottom:0;width:55%;height:65%}
</style></head>
<body>
<div id="menu"><h1>BLOCKWORLD</h1><button onclick="start()">▶ ИГРАТЬ</button><button onclick="alert('Мини-игры скоро будут добавлены!')">🎮 ИГРЫ</button></div>
<div id="game"><div id="world"><div id="hint">WASD / экранные зоны — движение<br>Правая часть — поворот камеры</div><div id="player"></div><div id="joy"></div><div id="look"></div></div></div>
<script>
function start(){menu.style.display='none';game.style.display='block'}
let p={x:50,y:55}; function move(dx,dy){p.x=Math.max(5,Math.min(95,p.x+dx));p.y=Math.max(8,Math.min(92,p.y+dy));player.style.left=p.x+'%';player.style.top=p.y+'%'}
document.addEventListener('keydown',e=>{if(e.key=='w'||e.key=='ArrowUp')move(0,-2);if(e.key=='s'||e.key=='ArrowDown')move(0,2);if(e.key=='a'||e.key=='ArrowLeft')move(-2,0);if(e.key=='d'||e.key=='ArrowRight')move(2,0)});
let sx=0,sy=0; look.addEventListener('touchstart',e=>{sx=e.touches[0].clientX;sy=e.touches[0].clientY});
look.addEventListener('touchmove',e=>{let t=e.touches[0];let dx=t.clientX-sx,dy=t.clientY-sy; sx=t.clientX;sy=t.clientY; world.style.transform='rotateY('+Math.max(-12,Math.min(12,(parseFloat(world.dataset.r||0)+dx*.04)))+'deg)';});
</script></body></html>"""
}
for path,data in files.items():
    full=os.path.join(root,path)
    os.makedirs(os.path.dirname(full),exist_ok=True)
    open(full,"w",encoding="utf-8").write(data)

zip_path="/mnt/data/BLOCKWORLD_Android_Project.zip"
with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
    for dp,_,fs in os.walk(root):
        for f in fs:
            fp=os.path.join(dp,f)
            z.write(fp,os.path.relpath(fp,root))

print(zip_path)
