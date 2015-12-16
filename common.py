import time
import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


partners_dic = {
    885: 'iris media',
    1152: 'sterkley',
    1259: 'sterkley',
    1516: 'sterkley',
    1506: 'sterkley',
    'dev': 'dev'
}


date_string = lambda x: x .strftime('%B %d, %Y %H:%M:%S')


def get_driver(driver_name):
    driver = None
    if driver_name == 'fox':
        driver = webdriver.Firefox()
    elif driver_name == 'ie':
        driver = webdriver.Ie()
    elif driver_name == 'chrome':
        driver = webdriver.Chrome()
    else:
        driver = 'driver not found'

    return driver


def close_driver(driver_object):
    try:
        driver_object.quit()
    except Exception as ex:
        print ex


def get_ctx_js(pid, aff_id):
    ctx = 'https://%s'
    if partners_dic.get(pid) == 'iris media':
        out = ctx % 'cjs.linkbolic.com/scjs/cjs/v10/ctxjs.js'
    elif partners_dic.get(pid) == 'sterkley':
        out = ctx % 'cjs.linkbolic.com/scjs/cjs/v9/ctxjs.js'
    elif partners_dic.get(pid) == 'dev':
        out = ctx % 'cjs.linkbolic.com/scjs/cjs/beta/ctxjs.js'
    else:
        out = ctx % 'cjs.linkbolic.com/scjs/cjs/ctxjs.js'

    return "%s?aff_id=%s&sbrand=testing" % (out, aff_id)


def injection_script(pid, aff_id):
    return """
 (function(d, script) {
    script = d.createElement('script');
    script.type = 'text/javascript';
    script.async = true;
    script.onload = function(){
        // remote script has loaded
    };
    script.src = '%s';
    d.getElementsByTagName('head')[0].appendChild(script);
}(document));
""" % get_ctx_js(pid, aff_id)


def increase_time(time_expresion, date):

    miliseconds = 0
    if time_expresion[-1] == 'm':
        miliseconds = int(time_expresion[:-1]) * 60 * 1000
    elif time_expresion[-1] == 's':
        miliseconds = int(time_expresion[:-1]) * 1000

    s = "timemachine.config({dateString:'%s',difference: %s});"

    print time_expresion, '->', miliseconds / 1000

    return s % (date_string(date), miliseconds)


def reset_time(time_expresion):
    return "timemachine.reset();"


def time_script_init(date):
    return ('!function(a,b){if("function"==typeof define)define(b);'
            'else if("undefined"!=typeof module&&module.exports)module.exports'
            '=b();else{var c=b(),d=this,e=d[a];c.noConflict=function(){return '
            'd[a]=e,c},d[a]=c}}("timemachine",function(){var a=Date,b='
            '{timestamp:0,tick:!1,tickStartDate:null,keepTime:!1,difference:0,'
            'config:function(b){this.timestamp=a.parse(b.dateString)||'
            'b.timestamp||this.timestamp,this.difference=b.difference||'
            'this.difference,this.keepTime=b.keepTime||this.keepTime,this.tick'
            '=b.tick||this.tick,this.tick&&(this.tickStartDate=new a),'
            'this._apply()},reset:function(){this.timestamp=0,this.tick=!1,'
            'this.tickStartDate=null,this.keepTime=!1,this.difference=0,Date=a,'
            'Date.prototype=a.prototype},_apply:function(){var b=this;Date='
            'function(){var c;c=b.keepTime?new a:1===arguments.length?new a'
            '(arguments[0]):7===arguments.length?new a(arguments[0],'
            'arguments[1],arguments[2],arguments[3],arguments[4],'
            'arguments[5],arguments[6]):new a(b.timestamp);var '
            'd=b._getDifference();return 0!==d&&(c=new a(c.getTime()+d)),c}'
            ',Date.prototype=a.prototype,Date.now=function(){var c=b.keepTime?'
            'a.now():b.timestamp;return c+b._getDifference()},'
            'Date.OriginalDate=a},_getDifference:function(){var '
            'b=this.difference;return this.tick&&(b+=a.now()-'
            'this.tickStartDate.getTime()),b}};return b._apply(),b});'
            'timemachine.config({ dateString: \'%s\'});') % date_string(date)


def body_click(driver):
    element = driver.find_element_by_tag_name('body')
    element.click()
    time.sleep(3)


def get_aff_id(pid):
    return int(float(pid))


def get_window_name(driver):
    return driver.execute_script("return window.name;")


def get_datetime(driver):
    return driver.execute_script("return new Date();")


def check_topbar(driver):

    try:
        driver.find_element_by_id('adsDiv06o815')
        return True
    except NoSuchElementException:
        return False
