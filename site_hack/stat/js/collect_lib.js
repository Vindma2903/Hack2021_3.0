async function post(url, data) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(await data);
}

async function get_components() {
    var obj = {};
    var components = await Fingerprint2.getPromise();
    for (var i = 0; i < components.length; i++) {
        if (['webgl', 'canvas'].indexOf(components[i].key) < 0) {
            obj[components[i].key] = components[i].value;
        }
    }
    var values = components.map(function (component) { return component.value });
    var murmur = Fingerprint2.x64hash128(values.join(''), 31);
    obj["murmur"] = murmur;
    return obj;
}

function get_gpu(data) {
    var name = "glcanvas";
    document.body.innerHTML += "    <canvas id=\"" + name + "\" width=\"1\" height=\"1\"></canvas>"
    var canvas = document.getElementById(name);
    var gl = canvas.getContext("experimental-webgl");
    if (gl) {
        var extension = gl.getExtension('WEBGL_debug_renderer_info');
        if (extension != undefined) {
            data["gpu_vendor"] = gl.getParameter(extension.UNMASKED_VENDOR_WEBGL);
            data["gpu_renderer"] = gl.getParameter(extension.UNMASKED_RENDERER_WEBGL);
        } else {
            data["gpu_vendor"] = gl.getParameter(gl.VENDOR);
            data["gpu_renderer"] = gl.getParameter(gl.RENDERER);
        }
    }
    return data;
}

async function get_battery(data) {
    if (!(navigator.getBattery || navigator.battery || navigator.mozBattery)) {
        return data;
    }
    var obj = {};
    const battery = await navigator.getBattery() || await navigator.battery() || await navigator.mozBattery();
    for (var key in battery) {
        var value = battery[key];
        obj[key] = value;
    }
    data["battery"] = obj;
    return data;
}

async function collect() {
    function versionMinor() {
        var versMajor = parseInt(navigator.appVersion,10);
        var appVers = navigator.appVersion;
        var pos, versMinor = 0;
        if ((pos = appVers.indexOf ("MSIE")) > -1) {
            versMinor = parseFloat(appVers.substr (pos+5));
        } else {
            versMinor = parseFloat(appVers);
        }
        return (versMinor);
    }
    var data = {};
    data["app_version"] = navigator.appVersion;
    data["version_mjr"] = parseInt(navigator.appVersion,10);
    data["version_mnr"] = versionMinor();
    data["screen_width"] = screen.width;
    data["screen_height"] = screen.height;
    data["inner_width"] = innerWidth;
    data["inner_height"] = innerHeight;
    data["java"] = navigator.javaEnabled();
    data["cookie"] = navigator.cookieEnabled;
    data["language"] = navigator.language;
    data["time"] = '' + new Date();
    data["utc"] = (0 - (new Date()).getTimezoneOffset())/60;
    data["user_agent"] = navigator.userAgent;
    data["os"] = navigator.platform;
    data["devices"] = await navigator.mediaDevices.enumerateDevices();
    data = await get_battery(data);
    data["components"] = await get_components();
    data = get_gpu(data);
    return JSON.stringify(data);
}

async function collect_and_next() {
    await post("/collect", collect());
    window.location = "/index";
}

async function collect_only() {
    await post("/collect", collect());
}
