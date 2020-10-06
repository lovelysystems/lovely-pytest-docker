from lovely.pytest.docker import url_checker


def test_url_checker():
    f = url_checker('/probe_status')
    assert f is not None
    assert f.args == ()
    assert f.keywords['path'] == '/probe_status'
