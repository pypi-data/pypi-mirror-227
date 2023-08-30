from datetime import datetime
import json

from pytest import raises

from typedpy import (
    String,
    Structure,
    ImmutableField,
    DateString,
    TimeString,
    EmailAddress,
    HostName,
    IPV4,
    JSONString,
    serialize,
    deserialize_structure,
    Integer,
)


class ImmutableString(String, ImmutableField):
    pass


class B(Structure):
    s = String(maxLength=5, minLength=2)
    a = ImmutableString()


def test_max_length_violation_err():
    with raises(ValueError) as excinfo:
        B(s="abcdef", a="")
    assert "s: Got 'abcdef'; Expected a maximum length of 5" in str(excinfo.value)


def test_min_length_violation_err():
    with raises(ValueError) as excinfo:
        B(s="a", a="")
    assert "s: Got 'a'; Expected a minimum length of 2" in str(excinfo.value)


def test_immutable_err():
    b = B(s="sss", a="asd")
    with raises(ValueError) as excinfo:
        b.a = "dd"
    assert "a: Field is immutable" in str(excinfo.value)


def test_date_err():
    class Example(Structure):
        d = DateString

    with raises(ValueError) as excinfo:
        Example(d="2017-99-99")
    assert (
        "d: Got '2017-99-99'; time data '2017-99-99' does not match format '%Y-%m-%d'"
        in str(excinfo.value)
    )


def test_date_valid():
    class Example(Structure):
        d = DateString

    e = Example(d="2017-8-9")
    assert datetime.strptime(e.d, "%Y-%m-%d").month == 8


def test_date_alternative_format_invalid():
    class Example(Structure):
        d = DateString(date_format="%Y%m%d")

    with raises(ValueError):
        Example(d="2017-8-9")


def test_date_alternative_format_serialization():
    class Example(Structure):
        d = DateString(date_format="%Y%m%d")
        i = Integer

    e = Example(d="19900530", i=5)
    assert deserialize_structure(Example, serialize(e)) == e


def test_date_alternative_format_valid():
    class Example(Structure):
        d = DateString(date_format="%Y%m%d")

    e = Example(d="20170809")
    assert datetime.strptime(e.d, "%Y%m%d").month == 8


def test_date_serialization():
    class Example(Structure):
        d = DateString

    e = Example(d="2017-8-9")
    assert deserialize_structure(Example, serialize(e)) == e


def test_time_err():
    class Example(Structure):
        t = TimeString

    with raises(ValueError) as excinfo:
        Example(t="20:1015")
    assert (
        "t: Got '20:1015'; time data '20:1015' does not match format '%H:%M:%S'"
        in str(excinfo.value)
    )


def test_time_valid():
    class Example(Structure):
        t = TimeString

    e = Example(t="20:10:15")
    assert datetime.strptime(e.t, "%H:%M:%S").hour == 20


def test_email_err():
    class Example(Structure):
        email = EmailAddress

    with raises(ValueError) as excinfo:
        Example(email="asdnsa@dsads.sds.")
    assert "email: Got 'asdnsa@dsads.sds.'; Does not match regular expression" in str(
        excinfo.value
    )


def test_email_valid():
    class Example(Structure):
        email = EmailAddress

    Example(email="abc@com.ddd").email == "abc@com.ddd"


def test_hostname_err():
    class Example(Structure):
        host = HostName

    with raises(ValueError) as excinfo:
        Example(host="aaa bbb")
    assert "host: Got 'aaa bbb'; wrong format for hostname" in str(excinfo.value)


def test_hostname_err2():
    class Example(Structure):
        host = HostName

    with raises(ValueError) as excinfo:
        Example(
            host="aaa.bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.asc"
        )
    assert (
        "host: Got 'aaa.bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.asc'; wrong format for hostname"
        in str(excinfo.value)
    )


def test_hostname_valid():
    class Example(Structure):
        host = HostName

    assert Example(host="com.ddd.dasdasdsadasdasda").host == "com.ddd.dasdasdsadasdasda"


def test_ipv4_err():
    class Example(Structure):
        ip = IPV4

    with raises(ValueError) as excinfo:
        Example(ip="2312.2222.223233")
    assert "ip: Got '2312.2222.223233'; wrong format for IP version 4" in str(
        excinfo.value
    )


def test_ipv4_valid():
    class Example(Structure):
        ip = IPV4

    assert Example(ip="212.22.33.192").ip.split(".") == ["212", "22", "33", "192"]


def test_JSONString_err():
    class Example(Structure):
        j = JSONString

    with raises(ValueError) as excinfo:
        Example(j="[1,2,3")


def test_JSONString_valid():
    class Example(Structure):
        j = JSONString

    assert json.loads(Example(j="[1,2,3]").j) == [1, 2, 3]


def test_get_of_field_that_is_unpopulated():
    class B(Structure):
        s = String(maxLength=5, minLength=2)
        a = ImmutableString()
        _required = []

    b = B(s="abcde")
    assert b.a is None


def test_get_of_field_that_is_unpopulated_with_default_value():
    class B(Structure):
        s = String(maxLength=5, minLength=2)
        a = ImmutableString(default="xyz")
        _required = []

    b = B(s="abcde")
    assert b.a == "xyz"
