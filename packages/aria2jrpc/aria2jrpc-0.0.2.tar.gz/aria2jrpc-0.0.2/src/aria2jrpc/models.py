from dataclasses import asdict, dataclass
from enum import Enum


class HowPosition(str, Enum):
    POST_SET = "POST_SET"
    POS_CUR = "POS_CUR"
    POS_END = "POS_END"


@dataclass
class Aria2CommonOptions:
    all_proxy: str | None = None
    all_proxy_passwd: str | None = None
    all_proxy_user: str | None = None
    allow_overwrite: str | None = None
    allow_piece_length_change: str | None = None
    always_resume: str | None = None
    async_dns: str | None = None
    auto_file_renaming: str | None = None
    bt_enable_hook_after_hash_check: str | None = None
    bt_enable_lpd: str | None = None
    bt_exclude_tracker: str | None = None
    bt_external_ip: str | None = None
    bt_force_encryption: str | None = None
    bt_hash_check_seed: str | None = None
    bt_load_saved_metadata: str | None = None
    bt_max_peers: str | None = None
    bt_metadata_only: str | None = None
    bt_min_crypto_level: str | None = None
    bt_prioritize_piece: str | None = None
    bt_remove_unselected_file: str | None = None
    bt_request_peer_speed_limit: str | None = None
    bt_require_crypto: str | None = None
    bt_save_metadata: str | None = None
    bt_seed_unverified: str | None = None
    bt_stop_timeout: str | None = None
    bt_tracker: str | None = None
    bt_tracker_connect_timeout: str | None = None
    bt_tracker_interval: str | None = None
    bt_tracker_timeout: str | None = None
    check_integrity: str | None = None
    conditional_get: str | None = None
    connect_timeout: str | None = None
    content_disposition_default_utf8: str | None = None
    continue_: str | None = None
    dir: str | None = None
    enable_http_keep_alive: str | None = None
    enable_http_pipelining: str | None = None
    enable_mmap: str | None = None
    enable_peer_exchange: str | None = None
    file_allocation: str | None = None
    follow_metalink: str | None = None
    follow_torrent: str | None = None
    force_save: str | None = None
    ftp_passwd: str | None = None
    ftp_pasv: str | None = None
    ftp_proxy: str | None = None
    ftp_proxy_passwd: str | None = None
    ftp_proxy_user: str | None = None
    ftp_reuse_connection: str | None = None
    ftp_type: str | None = None
    ftp_user: str | None = None
    gid: str | None = None
    hash_check_only: str | None = None
    header: str | None = None
    http_accept_gzip: str | None = None
    http_auth_challenge: str | None = None
    http_no_cache: str | None = None
    http_passwd: str | None = None
    http_proxy: str | None = None
    http_proxy_passwd: str | None = None
    http_proxy_user: str | None = None
    http_user: str | None = None
    https_proxy: str | None = None
    https_proxy_passwd: str | None = None
    https_proxy_user: str | None = None
    lowest_speed_limit: str | None = None
    max_connection_per_server: str | None = None
    max_download_limit: str | None = None
    max_file_not_found: str | None = None
    max_mmap_limit: str | None = None
    max_resume_failure_tries: str | None = None
    max_tries: str | None = None
    max_upload_limit: str | None = None
    metalink_enable_unique_protocol: str | None = None
    metalink_language: str | None = None
    metalink_location: str | None = None
    metalink_os: str | None = None
    metalink_preferred_protocol: str | None = None
    metalink_version: str | None = None
    min_split_size: str | None = None
    no_file_allocation_limit: str | None = None
    no_netrc: str | None = None
    no_proxy: str | None = None
    pause_metadata: str | None = None
    proxy_method: str | None = None
    realtime_chunk_checksum: str | None = None
    referer: str | None = None
    remote_time: str | None = None
    remove_control_file: str | None = None
    retry_wait: str | None = None
    reuse_uri: str | None = None
    seed_ratio: str | None = None
    seed_time: str | None = None
    split: str | None = None
    ssh_host_key_md: str | None = None
    stream_piece_selector: str | None = None
    timeout: str | None = None
    uri_selector: str | None = None
    use_head: str | None = None
    user_agent: str | None = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["continue"] = data.pop("continue_")
        data = {
            key.replace("_", "-"): str(value)
            for key, value in asdict(self).items()
            if value is not None
        }
        return data


@dataclass
class Aria2BaseOptions(Aria2CommonOptions):
    all_proxy: str | None = None
    all_proxy_passwd: str | None = None
    all_proxy_user: str | None = None
    allow_overwrite: str | None = None
    allow_piece_length_change: str | None = None
    always_resume: str | None = None
    async_dns: str | None = None
    auto_file_renaming: str | None = None
    bt_enable_hook_after_hash_check: str | None = None
    bt_enable_lpd: str | None = None
    bt_exclude_tracker: str | None = None
    bt_external_ip: str | None = None
    bt_force_encryption: str | None = None
    bt_hash_check_seed: str | None = None
    bt_load_saved_metadata: str | None = None
    bt_max_peers: str | None = None
    bt_metadata_only: str | None = None
    bt_min_crypto_level: str | None = None
    bt_prioritize_piece: str | None = None
    bt_remove_unselected_file: str | None = None
    bt_request_peer_speed_limit: str | None = None
    bt_require_crypto: str | None = None
    bt_save_metadata: str | None = None
    bt_seed_unverified: str | None = None
    bt_stop_timeout: str | None = None
    bt_tracker: str | None = None
    bt_tracker_connect_timeout: str | None = None
    bt_tracker_interval: str | None = None
    bt_tracker_timeout: str | None = None
    check_integrity: str | None = None
    conditional_get: str | None = None
    connect_timeout: str | None = None
    content_disposition_default_utf8: str | None = None
    continue_: str | None = None
    dir: str | None = None
    dry_run: str | None = None
    enable_http_keep_alive: str | None = None
    enable_http_pipelining: str | None = None
    enable_mmap: str | None = None
    enable_peer_exchange: str | None = None
    file_allocation: str | None = None
    follow_metalink: str | None = None
    follow_torrent: str | None = None
    force_save: str | None = None
    ftp_passwd: str | None = None
    ftp_pasv: str | None = None
    ftp_proxy: str | None = None
    ftp_proxy_passwd: str | None = None
    ftp_proxy_user: str | None = None
    ftp_reuse_connection: str | None = None
    ftp_type: str | None = None
    ftp_user: str | None = None
    gid: str | None = None
    hash_check_only: str | None = None
    header: str | None = None
    http_accept_gzip: str | None = None
    http_auth_challenge: str | None = None
    http_no_cache: str | None = None
    http_passwd: str | None = None
    http_proxy: str | None = None
    http_proxy_passwd: str | None = None
    http_proxy_user: str | None = None
    http_user: str | None = None
    https_proxy: str | None = None
    https_proxy_passwd: str | None = None
    https_proxy_user: str | None = None
    lowest_speed_limit: str | None = None
    max_connection_per_server: str | None = None
    max_download_limit: str | None = None
    max_file_not_found: str | None = None
    max_mmap_limit: str | None = None
    max_resume_failure_tries: str | None = None
    max_tries: str | None = None
    max_upload_limit: str | None = None
    metalink_base_uri: str | None = None
    metalink_enable_unique_protocol: str | None = None
    metalink_language: str | None = None
    metalink_location: str | None = None
    metalink_os: str | None = None
    metalink_preferred_protocol: str | None = None
    metalink_version: str | None = None
    min_split_size: str | None = None
    no_file_allocation_limit: str | None = None
    no_netrc: str | None = None
    no_proxy: str | None = None
    parameterized_uri: str | None = None
    pause_metadata: str | None = None
    piece_length: str | None = None
    proxy_method: str | None = None
    realtime_chunk_checksum: str | None = None
    referer: str | None = None
    remote_time: str | None = None
    remove_control_file: str | None = None
    retry_wait: str | None = None
    reuse_uri: str | None = None
    rpc_save_upload_metadata: str | None = None
    seed_ratio: str | None = None
    seed_time: str | None = None
    split: str | None = None
    ssh_host_key_md: str | None = None
    stream_piece_selector: str | None = None
    timeout: str | None = None
    uri_selector: str | None = None
    use_head: str | None = None
    user_agent: str | None = None


@dataclass
class Aria2InputOptions(Aria2BaseOptions):
    checksum: str | None = None
    index_out: str | None = None
    out: str | None = None
    pause: str | None = None
    select_file: str | None = None


@dataclass
class Aria2GlobalOptions(Aria2BaseOptions):
    bt_max_open_files: str | None = None
    download_result: str | None = None
    keep_unfinished_download_result: str | None = None
    log: str | None = None
    log_level: str | None = None
    max_concurrent_downloads: str | None = None
    max_download_result: str | None = None
    max_overall_download_limit: str | None = None
    max_overall_upload_limit: str | None = None
    optimize_concurrent_downloads: str | None = None
    save_cookies: str | None = None
    save_session: str | None = None
    server_stat_of: str | None = None
