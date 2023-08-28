import base64

import requests

from aria2jrpc.models import (
    Aria2CommonOptions,
    Aria2GlobalOptions,
    Aria2InputOptions,
    HowPosition,
)


class Aria2JRPC:
    def __init__(
        self,
        url: str,
        secret: str = "",
        global_options: Aria2GlobalOptions = Aria2GlobalOptions(),
    ) -> None:
        self._base_url = url + "/jsonrpc"
        self._secret = secret
        self._id = 1
        self._global_option = global_options
        self.change_global_option(global_options)

    def _get(
        self,
        method: str,
        params: list | None = [],
        id: str | None = None,
    ) -> dict:
        if not id:
            id = self._id
            self._id += 1
        params = [f"token:{self._secret}"] + params
        json_data = {
            "jsonrpc": "2.0",
            "method": method,
            "id": id,
            "params": params,
        }
        res = requests.post(
            self._base_url,
            json=json_data,
        )
        json_res = res.json()
        if error := json_res.get("error"):
            raise Exception(error["message"])
        return json_res

    def _download(
        self,
        method: str,
        options: Aria2InputOptions,
        position: int | None,
        params: list = [],
        id: str | None = None,
    ) -> dict:
        params.append(options.to_dict())
        if position is not None:
            params.append(position)
        return self._get(method, params, id)

    def add_uri(
        self,
        *uris: str,
        id: int | None = None,
        options: Aria2InputOptions | None = Aria2InputOptions(),
        position: int | None = None,
    ) -> str:
        return self._download(
            "aria2.addUri",
            id=id,
            params=[uris],
            options=options,
            position=position,
        )["result"]

    def add_torrent(
        self,
        *torrent_files_pathes: str,
        id: int | None = None,
        options: Aria2InputOptions | None = Aria2InputOptions(),
        position: int | None = None,
    ) -> str:
        torrents = []
        for torrent_file_path in torrent_files_pathes:
            with open(torrent_file_path, "r") as tf:
                base64.b64encode(tf.read())
        return self._download(
            "aria2.addTorrent",
            id=id,
            params=torrents,
            options=options,
            position=position,
        )["result"]

    def add_meta_link(
        self,
        *meta_file_pathes: str,
        id: int | None = None,
        options: Aria2InputOptions | None = Aria2InputOptions(),
        position: int | None = None,
    ) -> str:
        metas = []
        for torrent_file_path in meta_file_pathes:
            with open(torrent_file_path, "r") as tf:
                base64.b64encode(tf.read())
        return self._download(
            "aria2.addMetalink",
            id=id,
            params=metas,
            options=options,
            position=position,
        )["result"]

    def remove(
        self,
        gid: str,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.remove",
            id=id,
            params=[gid],
        )["result"]

    def force_remove(
        self,
        gid: str,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.forceRemove",
            id=id,
            params=[gid],
        )["result"]

    def pause(
        self,
        gid: str,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.pause",
            id=id,
            params=[gid],
        )["result"]

    def pause_all(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.pauseAll",
            id=id,
        )["result"]

    def force_pause(
        self,
        gid: str,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.forcePause",
            params=[gid],
            id=id,
        )["result"]

    def force_pause_all(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.forcePauseAll",
            id=id,
        )["result"]

    def unpause(
        self,
        gid: str,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.unpause",
            params=[gid],
            id=id,
        )["result"]

    def unpause_all(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.unpauseAll",
            id=id,
        )["result"]

    def tel_status(
        self,
        gid: str,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.tellStatus",
            params=[gid],
            id=id,
        )["result"]

    def get_uris(
        self,
        gid: str,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.getUris",
            params=[gid],
            id=id,
        )["result"]

    def get_files(
        self,
        gid: str,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.getFiles",
            params=[gid],
            id=id,
        )["result"]

    def get_peers(
        self,
        gid: str,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.getPeers",
            params=[gid],
            id=id,
        )["result"]

    def get_servers(
        self,
        gid: str,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.getServers",
            params=[gid],
            id=id,
        )["result"]

    def tel_active(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.tellActive",
            id=id,
        )["result"]

    def tel_waiting(
        self,
        offset: int = 0,
        num: int = 100,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.tellWaiting",
            params=[offset, num],
            id=id,
        )["result"]

    def tel_stopped(
        self,
        offset: int = 0,
        num: int = 100,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.tellStopped",
            params=[offset, num],
            id=id,
        )["result"]

    def change_position(
        self,
        gid: str,
        pos: int,
        how: HowPosition,
    ) -> str:
        return self._get(
            "aria2.getServers",
            params=[gid, pos, how.value],
            id=id,
        )["result"]

    def change_uri(
        self,
        gid: str,
        file_index: int,
        del_uris: list[str],
        add_uris: list[str],
    ) -> str:
        return self._get(
            "aria2.getServers",
            params=[gid, file_index, del_uris, add_uris],
            id=id,
        )["result"]

    def get_option(
        self,
        gid: str,
    ) -> dict:
        return self._get(
            "aria2.getOption",
            params=[gid],
            id=id,
        )["result"]

    def change_option(
        self,
        gid: str,
        options: Aria2CommonOptions,
    ) -> str:
        new_options = self.get_option(gid)
        new_options.update(options.to_dict())
        return self._get(
            "aria2.changeOption",
            params=[gid],
            id=id,
        )["result"]

    def get_global_option(
        self,
        id: int | None = None,
    ) -> dict:
        return self._get(
            "aria2.getGlobalOption",
            id=id,
        )["result"]

    def change_global_option(
        self,
        new_global_options: Aria2GlobalOptions,
        id: int | None = None,
    ) -> str:
        global_options = self.get_global_option()
        global_options.update(new_global_options.to_dict())
        return self._get(
            "aria2.changeGlobalOption",
            id=id,
            params=[global_options],
        )["result"]

    def get_global_stat(
        self,
        id: int | None = None,
    ) -> dict:
        return self._get(
            "aria2.getGlobalStat",
            id=id,
        )["result"]

    def purge_download_result(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.purgeDownloadResult",
            id=id,
        )["result"]

    def get_version(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "system.getVersion",
            id=id,
        )["result"]

    def get_session_info(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "system.getSessionInfo",
            id=id,
        )["result"]

    def shutdown(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.shutdown",
            id=id,
        )["result"]

    def force_shutdown(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.forceShutdown",
            id=id,
        )["result"]

    def save_session(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "aria2.saveSession",
            id=id,
        )["result"]

    def list_methods(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "system.listMethods",
            id=id,
        )["result"]

    def list_notifications(
        self,
        id: int | None = None,
    ) -> str:
        return self._get(
            "system.listNotifications",
            id=id,
        )["result"]


if __name__ == "__main__":
    my_aria = Aria2JRPC(
        "http://127.0.0.1:6800",
        secret="shitj",
        global_options=Aria2GlobalOptions(
            max_concurrent_downloads=1,
            continue_=1,
            max_connection_per_server=16,
            split=16,
            dir="d:/",
        ),
    )

    print(my_aria.list_notifications())
