import asyncio

import main


def shell_run(command):
    return {
        "Method": "Flow.Launcher.ShellRun",
        "Parameters": [f'start cmd.exe /K "{command}"', "cmd.exe"],
        "DontHideAfterAction": False,
    }


def test_unknown_command_shows_the_menu():
    results = list(main.query("foo"))
    assert [result.title for result in results] == ["search", "list"]
    assert all(result.icon == "icon.png" for result in results)


def test_empty_query_shows_the_menu():
    assert [result.title for result in main.query("")] == ["search", "list"]


def test_search_results_install_from_the_bucket_manifest(scoop, scoop_home):
    results = list(main.query("search 7zip"))
    path = str(scoop_home / "buckets" / "main" / "bucket" / "7zip.json")
    assert len(results) == 1
    result = results[0]
    assert result.title == "7zip (24.09)"
    assert result.subtitle == "A multi-format file archiver with high compression ratios"
    assert result.context_data == [path]
    assert result.json_rpc_action == shell_run(f"scoop install {path}")


def test_search_is_limited_to_25_results(scoop, scoop_home):
    bucket = scoop_home / "buckets" / "many" / "bucket"
    bucket.mkdir(parents=True)
    for n in range(30):
        (bucket / f"tool{n}.json").write_text('{"version": "1.0"}', encoding="utf-8")
    assert len(list(main.query("search tool"))) == 25


def test_search_skips_broken_manifests(scoop, scoop_home):
    (scoop_home / "buckets" / "main" / "bucket" / "gitbroken.json").write_text("{", encoding="utf-8")
    (scoop_home / "buckets" / "main" / "bucket" / "gitnoversion.json").write_text("{}", encoding="utf-8")
    titles = sorted(result.title for result in main.query("search git"))
    assert titles == ["git (2.47.1)", "git-lfs (3.6.0)", "gitkraken (10.5.0)"]


def test_list_shows_installed_apps(scoop):
    assert [result.title for result in main.query("list")] == ["git (2.47.1)", "7zip (24.09)"]


def test_context_menu_for_an_installed_app(scoop, scoop_home):
    path = scoop_home / "apps" / "git" / "2.47.1" / "manifest.json"
    results = list(main.context_menu([str(path)]))
    assert [result.title for result in results] == [
        "Uninstall git", "Update git", "Reveal in Explorer", "Open homepage",
    ]
    assert results[0].json_rpc_action == shell_run("scoop uninstall git")
    assert results[1].json_rpc_action == shell_run("scoop update git")
    assert results[2].json_rpc_action["Method"] == "Flow.Launcher.OpenDirectory"
    assert results[2].json_rpc_action["Parameters"] == [str(path.parent), str(path)]
    assert results[3].subtitle == "https://gitforwindows.org"
    assert results[3].json_rpc_action["Method"] == "Flow.Launcher.OpenUrl"
    assert results[3].json_rpc_action["Parameters"] == ["https://gitforwindows.org", False]


def test_context_menu_for_an_available_app_without_homepage(scoop, scoop_home):
    path = str(scoop_home / "buckets" / "main" / "bucket" / "elasticsearch.json")
    results = list(main.context_menu([path]))
    assert [result.title for result in results] == ["Install elasticsearch"]
    assert results[0].json_rpc_action == shell_run(f"scoop install {path}")


def test_query_through_the_plugin_dispatcher(scoop):
    response = asyncio.run(main.plugin._event_handler.trigger_event("query", "list"))
    assert [result["Title"] for result in response["Result"]] == ["git (2.47.1)", "7zip (24.09)"]
    assert response["Result"][0]["JsonRPCAction"]["Method"] == "Flow.Launcher.ShellRun"
