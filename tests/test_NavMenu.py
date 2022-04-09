
import pytest
import contextlib
from io import StringIO
from NavMenu import NavMenu


def test_navmenu_obj(supported_alg_names = ["A*", "Energy Cost A*"]):
    navmenu = NavMenu(supported_alg_names)
    
    assert not navmenu.env_created
    assert navmenu.env_dimensions == (0,0)
    assert navmenu.supported_alg_names == supported_alg_names
    assert len(navmenu._menu_relationship_map) == len(navmenu.menu_options)
    
    for menu_item in navmenu.menu_options.keys():
        assert menu_item in navmenu._menu_relationship_map.values()

def test_print_menu():
    navmenu = NavMenu(["A*", "Energy Cost A*"])
    with contextlib.redirect_stdout(StringIO()) as menu_output:
        navmenu.print_menu()
        for menu_item in navmenu.menu_options.keys():
            menu_output.seek(0)
            assert menu_item in menu_output.read()

def test_is_valid_option():
    navmenu = NavMenu(["A*", "Energy Cost A*"])
    assert navmenu.selection_is_valid_option("1")
    assert navmenu.selection_is_valid_option(2)
    assert navmenu.selection_is_valid_option("Create Environment")
    assert not navmenu.selection_is_valid_option("create")


@pytest.mark.parametrize("option",
    [
        ("hey"),
        #("create","is not a valid option, please enter another:")
    ]
)
def test_select_option(option):
    navmenu = NavMenu(["A*", "Energy Cost A*"])
    navmenu.menu_options = {"hey": it_works}
    with contextlib.redirect_stdout(StringIO()) as menu_output:
        navmenu.print_menu()
        navmenu.select_option(option)
        menu_output.seek(0)
        assert "It works" in menu_output.read()

def it_works():
    print("It works")