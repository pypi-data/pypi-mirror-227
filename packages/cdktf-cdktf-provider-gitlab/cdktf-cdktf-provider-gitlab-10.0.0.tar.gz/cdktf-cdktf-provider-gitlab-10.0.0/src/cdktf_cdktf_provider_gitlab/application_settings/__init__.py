'''
# `gitlab_application_settings`

Refer to the Terraform Registory for docs: [`gitlab_application_settings`](https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ApplicationSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-gitlab.applicationSettings.ApplicationSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings gitlab_application_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        abuse_notification_email: typing.Optional[builtins.str] = None,
        admin_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        after_sign_out_path: typing.Optional[builtins.str] = None,
        after_sign_up_text: typing.Optional[builtins.str] = None,
        akismet_api_key: typing.Optional[builtins.str] = None,
        akismet_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_group_owners_to_manage_ldap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_local_requests_from_system_hooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_local_requests_from_web_hooks_and_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        archive_builds_in_human_readable: typing.Optional[builtins.str] = None,
        asset_proxy_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
        asset_proxy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        asset_proxy_secret_key: typing.Optional[builtins.str] = None,
        asset_proxy_url: typing.Optional[builtins.str] = None,
        authorized_keys_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_devops_domain: typing.Optional[builtins.str] = None,
        auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        automatic_purchased_storage_allocation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        can_create_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        check_namespace_plan: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_email_hostname: typing.Optional[builtins.str] = None,
        container_expiration_policies_enable_historic_entries: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        container_registry_cleanup_tags_service_max_list_size: typing.Optional[jsii.Number] = None,
        container_registry_delete_tags_service_timeout: typing.Optional[jsii.Number] = None,
        container_registry_expiration_policies_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        container_registry_expiration_policies_worker_capacity: typing.Optional[jsii.Number] = None,
        container_registry_token_expire_delay: typing.Optional[jsii.Number] = None,
        deactivate_dormant_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_artifacts_expire_in: typing.Optional[builtins.str] = None,
        default_branch_name: typing.Optional[builtins.str] = None,
        default_branch_protection: typing.Optional[jsii.Number] = None,
        default_ci_config_path: typing.Optional[builtins.str] = None,
        default_group_visibility: typing.Optional[builtins.str] = None,
        default_project_creation: typing.Optional[jsii.Number] = None,
        default_projects_limit: typing.Optional[jsii.Number] = None,
        default_project_visibility: typing.Optional[builtins.str] = None,
        default_snippet_visibility: typing.Optional[builtins.str] = None,
        delayed_group_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delayed_project_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_inactive_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion_adjourned_period: typing.Optional[jsii.Number] = None,
        diff_max_files: typing.Optional[jsii.Number] = None,
        diff_max_lines: typing.Optional[jsii.Number] = None,
        diff_max_patch_bytes: typing.Optional[jsii.Number] = None,
        disabled_oauth_sign_in_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        disable_feed_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dns_rebinding_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        domain_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_denylist: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_denylist_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dsa_key_restriction: typing.Optional[jsii.Number] = None,
        ecdsa_key_restriction: typing.Optional[jsii.Number] = None,
        ecdsa_sk_key_restriction: typing.Optional[jsii.Number] = None,
        ed25519_key_restriction: typing.Optional[jsii.Number] = None,
        ed25519_sk_key_restriction: typing.Optional[jsii.Number] = None,
        eks_access_key_id: typing.Optional[builtins.str] = None,
        eks_account_id: typing.Optional[builtins.str] = None,
        eks_integration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        eks_secret_access_key: typing.Optional[builtins.str] = None,
        elasticsearch_aws: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        elasticsearch_aws_access_key: typing.Optional[builtins.str] = None,
        elasticsearch_aws_region: typing.Optional[builtins.str] = None,
        elasticsearch_aws_secret_access_key: typing.Optional[builtins.str] = None,
        elasticsearch_indexed_field_length_limit: typing.Optional[jsii.Number] = None,
        elasticsearch_indexed_file_size_limit_kb: typing.Optional[jsii.Number] = None,
        elasticsearch_indexing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        elasticsearch_limit_indexing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        elasticsearch_max_bulk_concurrency: typing.Optional[jsii.Number] = None,
        elasticsearch_max_bulk_size_mb: typing.Optional[jsii.Number] = None,
        elasticsearch_namespace_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        elasticsearch_password: typing.Optional[builtins.str] = None,
        elasticsearch_project_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        elasticsearch_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        elasticsearch_url: typing.Optional[typing.Sequence[builtins.str]] = None,
        elasticsearch_username: typing.Optional[builtins.str] = None,
        email_additional_text: typing.Optional[builtins.str] = None,
        email_author_in_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled_git_access_protocol: typing.Optional[builtins.str] = None,
        enforce_namespace_storage_limit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce_terms: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_auth_client_cert: typing.Optional[builtins.str] = None,
        external_auth_client_key: typing.Optional[builtins.str] = None,
        external_auth_client_key_pass: typing.Optional[builtins.str] = None,
        external_authorization_service_default_label: typing.Optional[builtins.str] = None,
        external_authorization_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_authorization_service_timeout: typing.Optional[jsii.Number] = None,
        external_authorization_service_url: typing.Optional[builtins.str] = None,
        external_pipeline_validation_service_timeout: typing.Optional[jsii.Number] = None,
        external_pipeline_validation_service_token: typing.Optional[builtins.str] = None,
        external_pipeline_validation_service_url: typing.Optional[builtins.str] = None,
        file_template_project_id: typing.Optional[jsii.Number] = None,
        first_day_of_week: typing.Optional[jsii.Number] = None,
        geo_node_allowed_ips: typing.Optional[builtins.str] = None,
        geo_status_timeout: typing.Optional[jsii.Number] = None,
        gitaly_timeout_default: typing.Optional[jsii.Number] = None,
        gitaly_timeout_fast: typing.Optional[jsii.Number] = None,
        gitaly_timeout_medium: typing.Optional[jsii.Number] = None,
        git_rate_limit_users_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
        git_two_factor_session_expiry: typing.Optional[jsii.Number] = None,
        grafana_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        grafana_url: typing.Optional[builtins.str] = None,
        gravatar_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_owners_can_manage_default_branch_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hashed_storage_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        help_page_hide_commercial_content: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        help_page_support_url: typing.Optional[builtins.str] = None,
        help_page_text: typing.Optional[builtins.str] = None,
        help_text: typing.Optional[builtins.str] = None,
        hide_third_party_offers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        home_page_url: typing.Optional[builtins.str] = None,
        housekeeping_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        housekeeping_full_repack_period: typing.Optional[jsii.Number] = None,
        housekeeping_gc_period: typing.Optional[jsii.Number] = None,
        housekeeping_incremental_repack_period: typing.Optional[jsii.Number] = None,
        html_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        import_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        inactive_projects_delete_after_months: typing.Optional[jsii.Number] = None,
        inactive_projects_min_size_mb: typing.Optional[jsii.Number] = None,
        inactive_projects_send_warning_email_after_months: typing.Optional[jsii.Number] = None,
        in_product_marketing_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        invisible_captcha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issues_create_limit: typing.Optional[jsii.Number] = None,
        keep_latest_artifact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        local_markdown_version: typing.Optional[jsii.Number] = None,
        mailgun_events_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mailgun_signing_key: typing.Optional[builtins.str] = None,
        maintenance_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maintenance_mode_message: typing.Optional[builtins.str] = None,
        max_artifacts_size: typing.Optional[jsii.Number] = None,
        max_attachment_size: typing.Optional[jsii.Number] = None,
        max_export_size: typing.Optional[jsii.Number] = None,
        max_import_size: typing.Optional[jsii.Number] = None,
        max_number_of_repository_downloads: typing.Optional[jsii.Number] = None,
        max_number_of_repository_downloads_within_time_period: typing.Optional[jsii.Number] = None,
        max_pages_size: typing.Optional[jsii.Number] = None,
        max_personal_access_token_lifetime: typing.Optional[jsii.Number] = None,
        max_ssh_key_lifetime: typing.Optional[jsii.Number] = None,
        metrics_method_call_threshold: typing.Optional[jsii.Number] = None,
        mirror_available: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mirror_capacity_threshold: typing.Optional[jsii.Number] = None,
        mirror_max_capacity: typing.Optional[jsii.Number] = None,
        mirror_max_delay: typing.Optional[jsii.Number] = None,
        npm_package_requests_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        outbound_local_requests_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
        package_registry_cleanup_policies_worker_capacity: typing.Optional[jsii.Number] = None,
        pages_domain_verification_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_authentication_enabled_for_git: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_authentication_enabled_for_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_lowercase_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_number_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_symbol_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_uppercase_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        performance_bar_allowed_group_path: typing.Optional[builtins.str] = None,
        personal_access_token_prefix: typing.Optional[builtins.str] = None,
        pipeline_limit_per_project_user_sha: typing.Optional[jsii.Number] = None,
        plantuml_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        plantuml_url: typing.Optional[builtins.str] = None,
        polling_interval_multiplier: typing.Optional[jsii.Number] = None,
        project_export_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prometheus_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protected_ci_variables: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        push_event_activities_limit: typing.Optional[jsii.Number] = None,
        push_event_hooks_limit: typing.Optional[jsii.Number] = None,
        pypi_package_requests_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rate_limiting_response_text: typing.Optional[builtins.str] = None,
        raw_blob_request_limit: typing.Optional[jsii.Number] = None,
        recaptcha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recaptcha_private_key: typing.Optional[builtins.str] = None,
        recaptcha_site_key: typing.Optional[builtins.str] = None,
        receive_max_input_size: typing.Optional[jsii.Number] = None,
        repository_checks_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        repository_size_limit: typing.Optional[jsii.Number] = None,
        repository_storages: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_storages_weighted: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
        require_admin_approval_after_user_signup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_two_factor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restricted_visibility_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        rsa_key_restriction: typing.Optional[jsii.Number] = None,
        search_rate_limit: typing.Optional[jsii.Number] = None,
        search_rate_limit_unauthenticated: typing.Optional[jsii.Number] = None,
        send_user_confirmation_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_expire_delay: typing.Optional[jsii.Number] = None,
        shared_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_runners_minutes: typing.Optional[jsii.Number] = None,
        shared_runners_text: typing.Optional[builtins.str] = None,
        sidekiq_job_limiter_compression_threshold_bytes: typing.Optional[jsii.Number] = None,
        sidekiq_job_limiter_limit_bytes: typing.Optional[jsii.Number] = None,
        sidekiq_job_limiter_mode: typing.Optional[builtins.str] = None,
        sign_in_text: typing.Optional[builtins.str] = None,
        signup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        slack_app_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        slack_app_id: typing.Optional[builtins.str] = None,
        slack_app_secret: typing.Optional[builtins.str] = None,
        slack_app_signing_secret: typing.Optional[builtins.str] = None,
        slack_app_verification_token: typing.Optional[builtins.str] = None,
        snippet_size_limit: typing.Optional[jsii.Number] = None,
        snowplow_app_id: typing.Optional[builtins.str] = None,
        snowplow_collector_hostname: typing.Optional[builtins.str] = None,
        snowplow_cookie_domain: typing.Optional[builtins.str] = None,
        snowplow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sourcegraph_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sourcegraph_public_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sourcegraph_url: typing.Optional[builtins.str] = None,
        spam_check_api_key: typing.Optional[builtins.str] = None,
        spam_check_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        spam_check_endpoint_url: typing.Optional[builtins.str] = None,
        suggest_pipeline_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        terminal_max_session_time: typing.Optional[jsii.Number] = None,
        terms: typing.Optional[builtins.str] = None,
        throttle_authenticated_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_authenticated_api_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_authenticated_api_requests_per_period: typing.Optional[jsii.Number] = None,
        throttle_authenticated_packages_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_authenticated_packages_api_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_authenticated_packages_api_requests_per_period: typing.Optional[jsii.Number] = None,
        throttle_authenticated_web_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_authenticated_web_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_authenticated_web_requests_per_period: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_unauthenticated_api_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_api_requests_per_period: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_packages_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_unauthenticated_packages_api_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_packages_api_requests_per_period: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_web_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_unauthenticated_web_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_web_requests_per_period: typing.Optional[jsii.Number] = None,
        time_tracking_limit_to_hours: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        two_factor_grace_period: typing.Optional[jsii.Number] = None,
        unique_ips_limit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unique_ips_limit_per_user: typing.Optional[jsii.Number] = None,
        unique_ips_limit_time_window: typing.Optional[jsii.Number] = None,
        usage_ping_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_deactivation_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_default_external: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_default_internal_regex: typing.Optional[builtins.str] = None,
        user_oauth_applications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_show_add_ssh_key_message: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        web_ide_clientside_preview_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        whats_new_variant: typing.Optional[builtins.str] = None,
        wiki_page_max_content_bytes: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings gitlab_application_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param abuse_notification_email: If set, abuse reports are sent to this address. Abuse reports are always available in the Admin Area. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#abuse_notification_email ApplicationSettings#abuse_notification_email}
        :param admin_mode: Require administrators to enable Admin Mode by re-authenticating for administrative tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#admin_mode ApplicationSettings#admin_mode}
        :param after_sign_out_path: Where to redirect users after logout. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#after_sign_out_path ApplicationSettings#after_sign_out_path}
        :param after_sign_up_text: Text shown to the user after signing up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#after_sign_up_text ApplicationSettings#after_sign_up_text}
        :param akismet_api_key: API key for Akismet spam protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#akismet_api_key ApplicationSettings#akismet_api_key}
        :param akismet_enabled: (If enabled, requires: akismet_api_key) Enable or disable Akismet spam protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#akismet_enabled ApplicationSettings#akismet_enabled}
        :param allow_group_owners_to_manage_ldap: Set to true to allow group owners to manage LDAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#allow_group_owners_to_manage_ldap ApplicationSettings#allow_group_owners_to_manage_ldap}
        :param allow_local_requests_from_system_hooks: Allow requests to the local network from system hooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#allow_local_requests_from_system_hooks ApplicationSettings#allow_local_requests_from_system_hooks}
        :param allow_local_requests_from_web_hooks_and_services: Allow requests to the local network from web hooks and services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#allow_local_requests_from_web_hooks_and_services ApplicationSettings#allow_local_requests_from_web_hooks_and_services}
        :param archive_builds_in_human_readable: Set the duration for which the jobs are considered as old and expired. After that time passes, the jobs are archived and no longer able to be retried. Make it empty to never expire jobs. It has to be no less than 1 day, for example: 15 days, 1 month, 2 years. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#archive_builds_in_human_readable ApplicationSettings#archive_builds_in_human_readable}
        :param asset_proxy_allowlist: Assets that match these domains are not proxied. Wildcards allowed. Your GitLab installation URL is automatically allowlisted. GitLab restart is required to apply changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_allowlist ApplicationSettings#asset_proxy_allowlist}
        :param asset_proxy_enabled: (If enabled, requires: asset_proxy_url) Enable proxying of assets. GitLab restart is required to apply changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_enabled ApplicationSettings#asset_proxy_enabled}
        :param asset_proxy_secret_key: Shared secret with the asset proxy server. GitLab restart is required to apply changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_secret_key ApplicationSettings#asset_proxy_secret_key}
        :param asset_proxy_url: URL of the asset proxy server. GitLab restart is required to apply changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_url ApplicationSettings#asset_proxy_url}
        :param authorized_keys_enabled: By default, we write to the authorized_keys file to support Git over SSH without additional configuration. GitLab can be optimized to authenticate SSH keys via the database file. Only disable this if you have configured your OpenSSH server to use the AuthorizedKeysCommand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#authorized_keys_enabled ApplicationSettings#authorized_keys_enabled}
        :param auto_devops_domain: Specify a domain to use by default for every project’s Auto Review Apps and Auto Deploy stages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#auto_devops_domain ApplicationSettings#auto_devops_domain}
        :param auto_devops_enabled: Enable Auto DevOps for projects by default. It automatically builds, tests, and deploys applications based on a predefined CI/CD configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#auto_devops_enabled ApplicationSettings#auto_devops_enabled}
        :param automatic_purchased_storage_allocation: Enabling this permits automatic allocation of purchased storage in a namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#automatic_purchased_storage_allocation ApplicationSettings#automatic_purchased_storage_allocation}
        :param can_create_group: Indicates whether users can create top-level groups. Introduced in GitLab 15.5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#can_create_group ApplicationSettings#can_create_group}
        :param check_namespace_plan: Enabling this makes only licensed EE features available to projects if the project namespace’s plan includes the feature or if the project is public. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#check_namespace_plan ApplicationSettings#check_namespace_plan}
        :param commit_email_hostname: Custom hostname (for private commit emails). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#commit_email_hostname ApplicationSettings#commit_email_hostname}
        :param container_expiration_policies_enable_historic_entries: Enable cleanup policies for all projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_expiration_policies_enable_historic_entries ApplicationSettings#container_expiration_policies_enable_historic_entries}
        :param container_registry_cleanup_tags_service_max_list_size: The maximum number of tags that can be deleted in a single execution of cleanup policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_cleanup_tags_service_max_list_size ApplicationSettings#container_registry_cleanup_tags_service_max_list_size}
        :param container_registry_delete_tags_service_timeout: The maximum time, in seconds, that the cleanup process can take to delete a batch of tags for cleanup policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_delete_tags_service_timeout ApplicationSettings#container_registry_delete_tags_service_timeout}
        :param container_registry_expiration_policies_caching: Caching during the execution of cleanup policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_expiration_policies_caching ApplicationSettings#container_registry_expiration_policies_caching}
        :param container_registry_expiration_policies_worker_capacity: Number of workers for cleanup policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_expiration_policies_worker_capacity ApplicationSettings#container_registry_expiration_policies_worker_capacity}
        :param container_registry_token_expire_delay: Container Registry token duration in minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_token_expire_delay ApplicationSettings#container_registry_token_expire_delay}
        :param deactivate_dormant_users: Enable automatic deactivation of dormant users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#deactivate_dormant_users ApplicationSettings#deactivate_dormant_users}
        :param default_artifacts_expire_in: Set the default expiration time for each job’s artifacts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_artifacts_expire_in ApplicationSettings#default_artifacts_expire_in}
        :param default_branch_name: Instance-level custom initial branch name (introduced in GitLab 13.2). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_branch_name ApplicationSettings#default_branch_name}
        :param default_branch_protection: Determine if developers can push to the default branch. Can take: 0 (not protected, both users with the Developer role or Maintainer role can push new commits and force push), 1 (partially protected, users with the Developer role or Maintainer role can push new commits, but cannot force push) or 2 (fully protected, users with the Developer or Maintainer role cannot push new commits, but users with the Developer or Maintainer role can; no one can force push) as a parameter. Default is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_branch_protection ApplicationSettings#default_branch_protection}
        :param default_ci_config_path: Default CI/CD configuration file and path for new projects (.gitlab-ci.yml if not set). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_ci_config_path ApplicationSettings#default_ci_config_path}
        :param default_group_visibility: What visibility level new groups receive. Can take private, internal and public as a parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_group_visibility ApplicationSettings#default_group_visibility}
        :param default_project_creation: Default project creation protection. Can take: 0 (No one), 1 (Maintainers) or 2 (Developers + Maintainers). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_project_creation ApplicationSettings#default_project_creation}
        :param default_projects_limit: Project limit per user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_projects_limit ApplicationSettings#default_projects_limit}
        :param default_project_visibility: What visibility level new projects receive. Can take private, internal and public as a parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_project_visibility ApplicationSettings#default_project_visibility}
        :param default_snippet_visibility: What visibility level new snippets receive. Can take private, internal and public as a parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_snippet_visibility ApplicationSettings#default_snippet_visibility}
        :param delayed_group_deletion: Enable delayed group deletion. Introduced in GitLab 15.0. From GitLab 15.1, disables and locks the group-level setting for delayed protect deletion when set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#delayed_group_deletion ApplicationSettings#delayed_group_deletion}
        :param delayed_project_deletion: Enable delayed project deletion by default in new groups. From GitLab 15.1, can only be enabled when delayed_group_deletion is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#delayed_project_deletion ApplicationSettings#delayed_project_deletion}
        :param delete_inactive_projects: Enable inactive project deletion feature. Introduced in GitLab 14.10. Became operational in GitLab 15.0 (with feature flag inactive_projects_deletion). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#delete_inactive_projects ApplicationSettings#delete_inactive_projects}
        :param deletion_adjourned_period: The number of days to wait before deleting a project or group that is marked for deletion. Value must be between 1 and 90. From GitLab 15.1, a hook on deletion_adjourned_period sets the period to 1 on every update, and sets both delayed_project_deletion and delayed_group_deletion to false if the period is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#deletion_adjourned_period ApplicationSettings#deletion_adjourned_period}
        :param diff_max_files: Maximum files in a diff. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#diff_max_files ApplicationSettings#diff_max_files}
        :param diff_max_lines: Maximum lines in a diff. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#diff_max_lines ApplicationSettings#diff_max_lines}
        :param diff_max_patch_bytes: Maximum diff patch size, in bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#diff_max_patch_bytes ApplicationSettings#diff_max_patch_bytes}
        :param disabled_oauth_sign_in_sources: Disabled OAuth sign-in sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#disabled_oauth_sign_in_sources ApplicationSettings#disabled_oauth_sign_in_sources}
        :param disable_feed_token: Disable display of RSS/Atom and calendar feed tokens (introduced in GitLab 13.7). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#disable_feed_token ApplicationSettings#disable_feed_token}
        :param dns_rebinding_protection_enabled: Enforce DNS rebinding attack protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#dns_rebinding_protection_enabled ApplicationSettings#dns_rebinding_protection_enabled}
        :param domain_allowlist: Force people to use only corporate emails for sign-up. Null means there is no restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#domain_allowlist ApplicationSettings#domain_allowlist}
        :param domain_denylist: Users with email addresses that match these domains cannot sign up. Wildcards allowed. Use separate lines for multiple entries. Ex: domain.com, *.domain.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#domain_denylist ApplicationSettings#domain_denylist}
        :param domain_denylist_enabled: (If enabled, requires: domain_denylist) Allows blocking sign-ups from emails from specific domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#domain_denylist_enabled ApplicationSettings#domain_denylist_enabled}
        :param dsa_key_restriction: The minimum allowed bit length of an uploaded DSA key. 0 means no restriction. -1 disables DSA keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#dsa_key_restriction ApplicationSettings#dsa_key_restriction}
        :param ecdsa_key_restriction: The minimum allowed curve size (in bits) of an uploaded ECDSA key. 0 means no restriction. -1 disables ECDSA keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ecdsa_key_restriction ApplicationSettings#ecdsa_key_restriction}
        :param ecdsa_sk_key_restriction: The minimum allowed curve size (in bits) of an uploaded ECDSA_SK key. 0 means no restriction. -1 disables ECDSA_SK keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ecdsa_sk_key_restriction ApplicationSettings#ecdsa_sk_key_restriction}
        :param ed25519_key_restriction: The minimum allowed curve size (in bits) of an uploaded ED25519 key. 0 means no restriction. -1 disables ED25519 keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ed25519_key_restriction ApplicationSettings#ed25519_key_restriction}
        :param ed25519_sk_key_restriction: The minimum allowed curve size (in bits) of an uploaded ED25519_SK key. 0 means no restriction. -1 disables ED25519_SK keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ed25519_sk_key_restriction ApplicationSettings#ed25519_sk_key_restriction}
        :param eks_access_key_id: AWS IAM access key ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_access_key_id ApplicationSettings#eks_access_key_id}
        :param eks_account_id: Amazon account ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_account_id ApplicationSettings#eks_account_id}
        :param eks_integration_enabled: Enable integration with Amazon EKS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_integration_enabled ApplicationSettings#eks_integration_enabled}
        :param eks_secret_access_key: AWS IAM secret access key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_secret_access_key ApplicationSettings#eks_secret_access_key}
        :param elasticsearch_aws: Enable the use of AWS hosted Elasticsearch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws ApplicationSettings#elasticsearch_aws}
        :param elasticsearch_aws_access_key: AWS IAM access key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws_access_key ApplicationSettings#elasticsearch_aws_access_key}
        :param elasticsearch_aws_region: The AWS region the Elasticsearch domain is configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws_region ApplicationSettings#elasticsearch_aws_region}
        :param elasticsearch_aws_secret_access_key: AWS IAM secret access key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws_secret_access_key ApplicationSettings#elasticsearch_aws_secret_access_key}
        :param elasticsearch_indexed_field_length_limit: Maximum size of text fields to index by Elasticsearch. 0 value means no limit. This does not apply to repository and wiki indexing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_indexed_field_length_limit ApplicationSettings#elasticsearch_indexed_field_length_limit}
        :param elasticsearch_indexed_file_size_limit_kb: Maximum size of repository and wiki files that are indexed by Elasticsearch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_indexed_file_size_limit_kb ApplicationSettings#elasticsearch_indexed_file_size_limit_kb}
        :param elasticsearch_indexing: Enable Elasticsearch indexing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_indexing ApplicationSettings#elasticsearch_indexing}
        :param elasticsearch_limit_indexing: Limit Elasticsearch to index certain namespaces and projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_limit_indexing ApplicationSettings#elasticsearch_limit_indexing}
        :param elasticsearch_max_bulk_concurrency: Maximum concurrency of Elasticsearch bulk requests per indexing operation. This only applies to repository indexing operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_max_bulk_concurrency ApplicationSettings#elasticsearch_max_bulk_concurrency}
        :param elasticsearch_max_bulk_size_mb: Maximum size of Elasticsearch bulk indexing requests in MB. This only applies to repository indexing operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_max_bulk_size_mb ApplicationSettings#elasticsearch_max_bulk_size_mb}
        :param elasticsearch_namespace_ids: The namespaces to index via Elasticsearch if elasticsearch_limit_indexing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_namespace_ids ApplicationSettings#elasticsearch_namespace_ids}
        :param elasticsearch_password: The password of your Elasticsearch instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_password ApplicationSettings#elasticsearch_password}
        :param elasticsearch_project_ids: The projects to index via Elasticsearch if elasticsearch_limit_indexing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_project_ids ApplicationSettings#elasticsearch_project_ids}
        :param elasticsearch_search: Enable Elasticsearch search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_search ApplicationSettings#elasticsearch_search}
        :param elasticsearch_url: The URL to use for connecting to Elasticsearch. Use a comma-separated list to support cluster (for example, http://localhost:9200, http://localhost:9201). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_url ApplicationSettings#elasticsearch_url}
        :param elasticsearch_username: The username of your Elasticsearch instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_username ApplicationSettings#elasticsearch_username}
        :param email_additional_text: Additional text added to the bottom of every email for legal/auditing/compliance reasons. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#email_additional_text ApplicationSettings#email_additional_text}
        :param email_author_in_body: Some email servers do not support overriding the email sender name. Enable this option to include the name of the author of the issue, merge request or comment in the email body instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#email_author_in_body ApplicationSettings#email_author_in_body}
        :param enabled_git_access_protocol: Enabled protocols for Git access. Allowed values are: ssh, http, and nil to allow both protocols. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#enabled_git_access_protocol ApplicationSettings#enabled_git_access_protocol}
        :param enforce_namespace_storage_limit: Enabling this permits enforcement of namespace storage limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#enforce_namespace_storage_limit ApplicationSettings#enforce_namespace_storage_limit}
        :param enforce_terms: (If enabled, requires: terms) Enforce application ToS to all users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#enforce_terms ApplicationSettings#enforce_terms}
        :param external_auth_client_cert: (If enabled, requires: external_auth_client_key) The certificate to use to authenticate with the external authorization service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_auth_client_cert ApplicationSettings#external_auth_client_cert}
        :param external_auth_client_key: Private key for the certificate when authentication is required for the external authorization service, this is encrypted when stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_auth_client_key ApplicationSettings#external_auth_client_key}
        :param external_auth_client_key_pass: Passphrase to use for the private key when authenticating with the external service this is encrypted when stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_auth_client_key_pass ApplicationSettings#external_auth_client_key_pass}
        :param external_authorization_service_default_label: The default classification label to use when requesting authorization and no classification label has been specified on the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_default_label ApplicationSettings#external_authorization_service_default_label}
        :param external_authorization_service_enabled: (If enabled, requires: external_authorization_service_default_label, external_authorization_service_timeout and external_authorization_service_url) Enable using an external authorization service for accessing projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_enabled ApplicationSettings#external_authorization_service_enabled}
        :param external_authorization_service_timeout: The timeout after which an authorization request is aborted, in seconds. When a request times out, access is denied to the user. (min: 0.001, max: 10, step: 0.001). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_timeout ApplicationSettings#external_authorization_service_timeout}
        :param external_authorization_service_url: URL to which authorization requests are directed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_url ApplicationSettings#external_authorization_service_url}
        :param external_pipeline_validation_service_timeout: How long to wait for a response from the pipeline validation service. Assumes OK if it times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_pipeline_validation_service_timeout ApplicationSettings#external_pipeline_validation_service_timeout}
        :param external_pipeline_validation_service_token: Optional. Token to include as the X-Gitlab-Token header in requests to the URL in external_pipeline_validation_service_url. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_pipeline_validation_service_token ApplicationSettings#external_pipeline_validation_service_token}
        :param external_pipeline_validation_service_url: URL to use for pipeline validation requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_pipeline_validation_service_url ApplicationSettings#external_pipeline_validation_service_url}
        :param file_template_project_id: The ID of a project to load custom file templates from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#file_template_project_id ApplicationSettings#file_template_project_id}
        :param first_day_of_week: Start day of the week for calendar views and date pickers. Valid values are 0 for Sunday, 1 for Monday, and 6 for Saturday. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#first_day_of_week ApplicationSettings#first_day_of_week}
        :param geo_node_allowed_ips: Comma-separated list of IPs and CIDRs of allowed secondary nodes. For example, 1.1.1.1, 2.2.2.0/24. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#geo_node_allowed_ips ApplicationSettings#geo_node_allowed_ips}
        :param geo_status_timeout: The amount of seconds after which a request to get a secondary node status times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#geo_status_timeout ApplicationSettings#geo_status_timeout}
        :param gitaly_timeout_default: Default Gitaly timeout, in seconds. This timeout is not enforced for Git fetch/push operations or Sidekiq jobs. Set to 0 to disable timeouts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gitaly_timeout_default ApplicationSettings#gitaly_timeout_default}
        :param gitaly_timeout_fast: Gitaly fast operation timeout, in seconds. Some Gitaly operations are expected to be fast. If they exceed this threshold, there may be a problem with a storage shard and ‘failing fast’ can help maintain the stability of the GitLab instance. Set to 0 to disable timeouts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gitaly_timeout_fast ApplicationSettings#gitaly_timeout_fast}
        :param gitaly_timeout_medium: Medium Gitaly timeout, in seconds. This should be a value between the Fast and the Default timeout. Set to 0 to disable timeouts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gitaly_timeout_medium ApplicationSettings#gitaly_timeout_medium}
        :param git_rate_limit_users_allowlist: List of usernames excluded from Git anti-abuse rate limits. Maximum: 100 usernames. Introduced in GitLab 15.2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#git_rate_limit_users_allowlist ApplicationSettings#git_rate_limit_users_allowlist}
        :param git_two_factor_session_expiry: Maximum duration (in minutes) of a session for Git operations when 2FA is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#git_two_factor_session_expiry ApplicationSettings#git_two_factor_session_expiry}
        :param grafana_enabled: Enable Grafana. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#grafana_enabled ApplicationSettings#grafana_enabled}
        :param grafana_url: Grafana URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#grafana_url ApplicationSettings#grafana_url}
        :param gravatar_enabled: Enable Gravatar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gravatar_enabled ApplicationSettings#gravatar_enabled}
        :param group_owners_can_manage_default_branch_protection: Prevent overrides of default branch protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#group_owners_can_manage_default_branch_protection ApplicationSettings#group_owners_can_manage_default_branch_protection}
        :param hashed_storage_enabled: Create new projects using hashed storage paths: Enable immutable, hash-based paths and repository names to store repositories on disk. This prevents repositories from having to be moved or renamed when the Project URL changes and may improve disk I/O performance. (Always enabled in GitLab versions 13.0 and later, configuration is scheduled for removal in 14.0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#hashed_storage_enabled ApplicationSettings#hashed_storage_enabled}
        :param help_page_hide_commercial_content: Hide marketing-related entries from help. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_page_hide_commercial_content ApplicationSettings#help_page_hide_commercial_content}
        :param help_page_support_url: Alternate support URL for help page and help dropdown. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_page_support_url ApplicationSettings#help_page_support_url}
        :param help_page_text: Custom text displayed on the help page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_page_text ApplicationSettings#help_page_text}
        :param help_text: GitLab server administrator information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_text ApplicationSettings#help_text}
        :param hide_third_party_offers: Do not display offers from third parties in GitLab. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#hide_third_party_offers ApplicationSettings#hide_third_party_offers}
        :param home_page_url: Redirect to this URL when not logged in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#home_page_url ApplicationSettings#home_page_url}
        :param housekeeping_enabled: (If enabled, requires: housekeeping_bitmaps_enabled, housekeeping_full_repack_period, housekeeping_gc_period, and housekeeping_incremental_repack_period) Enable or disable Git housekeeping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_enabled ApplicationSettings#housekeeping_enabled}
        :param housekeeping_full_repack_period: Number of Git pushes after which an incremental git repack is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_full_repack_period ApplicationSettings#housekeeping_full_repack_period}
        :param housekeeping_gc_period: Number of Git pushes after which git gc is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_gc_period ApplicationSettings#housekeeping_gc_period}
        :param housekeeping_incremental_repack_period: Number of Git pushes after which an incremental git repack is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_incremental_repack_period ApplicationSettings#housekeeping_incremental_repack_period}
        :param html_emails_enabled: Enable HTML emails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#html_emails_enabled ApplicationSettings#html_emails_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#id ApplicationSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_sources: Sources to allow project import from. Valid values are: ``github``, ``bitbucket``, ``bitbucket_server``, ``fogbugz``, ``git``, ``gitlab_project``, ``gitea``, ``manifest``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#import_sources ApplicationSettings#import_sources}
        :param inactive_projects_delete_after_months: If delete_inactive_projects is true, the time (in months) to wait before deleting inactive projects. Introduced in GitLab 14.10. Became operational in GitLab 15.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#inactive_projects_delete_after_months ApplicationSettings#inactive_projects_delete_after_months}
        :param inactive_projects_min_size_mb: If delete_inactive_projects is true, the minimum repository size for projects to be checked for inactivity. Introduced in GitLab 14.10. Became operational in GitLab 15.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#inactive_projects_min_size_mb ApplicationSettings#inactive_projects_min_size_mb}
        :param inactive_projects_send_warning_email_after_months: If delete_inactive_projects is true, sets the time (in months) to wait before emailing maintainers that the project is scheduled be deleted because it is inactive. Introduced in GitLab 14.10. Became operational in GitLab 15.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#inactive_projects_send_warning_email_after_months ApplicationSettings#inactive_projects_send_warning_email_after_months}
        :param in_product_marketing_emails_enabled: Enable in-product marketing emails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#in_product_marketing_emails_enabled ApplicationSettings#in_product_marketing_emails_enabled}
        :param invisible_captcha_enabled: Enable Invisible CAPTCHA spam detection during sign-up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#invisible_captcha_enabled ApplicationSettings#invisible_captcha_enabled}
        :param issues_create_limit: Max number of issue creation requests per minute per user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#issues_create_limit ApplicationSettings#issues_create_limit}
        :param keep_latest_artifact: Prevent the deletion of the artifacts from the most recent successful jobs, regardless of the expiry time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#keep_latest_artifact ApplicationSettings#keep_latest_artifact}
        :param local_markdown_version: Increase this value when any cached Markdown should be invalidated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#local_markdown_version ApplicationSettings#local_markdown_version}
        :param mailgun_events_enabled: Enable Mailgun event receiver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mailgun_events_enabled ApplicationSettings#mailgun_events_enabled}
        :param mailgun_signing_key: The Mailgun HTTP webhook signing key for receiving events from webhook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mailgun_signing_key ApplicationSettings#mailgun_signing_key}
        :param maintenance_mode: When instance is in maintenance mode, non-administrative users can sign in with read-only access and make read-only API requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#maintenance_mode ApplicationSettings#maintenance_mode}
        :param maintenance_mode_message: Message displayed when instance is in maintenance mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#maintenance_mode_message ApplicationSettings#maintenance_mode_message}
        :param max_artifacts_size: Maximum artifacts size in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_artifacts_size ApplicationSettings#max_artifacts_size}
        :param max_attachment_size: Limit attachment size in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_attachment_size ApplicationSettings#max_attachment_size}
        :param max_export_size: Maximum export size in MB. 0 for unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_export_size ApplicationSettings#max_export_size}
        :param max_import_size: Maximum import size in MB. 0 for unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_import_size ApplicationSettings#max_import_size}
        :param max_number_of_repository_downloads: Maximum number of unique repositories a user can download in the specified time period before they are banned. Maximum: 10,000 repositories. Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_number_of_repository_downloads ApplicationSettings#max_number_of_repository_downloads}
        :param max_number_of_repository_downloads_within_time_period: Reporting time period (in seconds). Maximum: 864000 seconds (10 days). Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_number_of_repository_downloads_within_time_period ApplicationSettings#max_number_of_repository_downloads_within_time_period}
        :param max_pages_size: Maximum size of pages repositories in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_pages_size ApplicationSettings#max_pages_size}
        :param max_personal_access_token_lifetime: Maximum allowable lifetime for access tokens in days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_personal_access_token_lifetime ApplicationSettings#max_personal_access_token_lifetime}
        :param max_ssh_key_lifetime: Maximum allowable lifetime for SSH keys in days. Introduced in GitLab 14.6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_ssh_key_lifetime ApplicationSettings#max_ssh_key_lifetime}
        :param metrics_method_call_threshold: A method call is only tracked when it takes longer than the given amount of milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#metrics_method_call_threshold ApplicationSettings#metrics_method_call_threshold}
        :param mirror_available: Allow repository mirroring to configured by project Maintainers. If disabled, only Administrators can configure repository mirroring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_available ApplicationSettings#mirror_available}
        :param mirror_capacity_threshold: Minimum capacity to be available before scheduling more mirrors preemptively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_capacity_threshold ApplicationSettings#mirror_capacity_threshold}
        :param mirror_max_capacity: Maximum number of mirrors that can be synchronizing at the same time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_max_capacity ApplicationSettings#mirror_max_capacity}
        :param mirror_max_delay: Maximum time (in minutes) between updates that a mirror can have when scheduled to synchronize. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_max_delay ApplicationSettings#mirror_max_delay}
        :param npm_package_requests_forwarding: Use npmjs.org as a default remote repository when the package is not found in the GitLab Package Registry for npm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#npm_package_requests_forwarding ApplicationSettings#npm_package_requests_forwarding}
        :param outbound_local_requests_whitelist: Define a list of trusted domains or IP addresses to which local requests are allowed when local requests for hooks and services are disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#outbound_local_requests_whitelist ApplicationSettings#outbound_local_requests_whitelist}
        :param package_registry_cleanup_policies_worker_capacity: Number of workers assigned to the packages cleanup policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#package_registry_cleanup_policies_worker_capacity ApplicationSettings#package_registry_cleanup_policies_worker_capacity}
        :param pages_domain_verification_enabled: Require users to prove ownership of custom domains. Domain verification is an essential security measure for public GitLab sites. Users are required to demonstrate they control a domain before it is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#pages_domain_verification_enabled ApplicationSettings#pages_domain_verification_enabled}
        :param password_authentication_enabled_for_git: Enable authentication for Git over HTTP(S) via a GitLab account password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_authentication_enabled_for_git ApplicationSettings#password_authentication_enabled_for_git}
        :param password_authentication_enabled_for_web: Enable authentication for the web interface via a GitLab account password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_authentication_enabled_for_web ApplicationSettings#password_authentication_enabled_for_web}
        :param password_lowercase_required: Indicates whether passwords require at least one lowercase letter. Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_lowercase_required ApplicationSettings#password_lowercase_required}
        :param password_number_required: Indicates whether passwords require at least one number. Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_number_required ApplicationSettings#password_number_required}
        :param password_symbol_required: Indicates whether passwords require at least one symbol character. Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_symbol_required ApplicationSettings#password_symbol_required}
        :param password_uppercase_required: Indicates whether passwords require at least one uppercase letter. Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_uppercase_required ApplicationSettings#password_uppercase_required}
        :param performance_bar_allowed_group_path: Path of the group that is allowed to toggle the performance bar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#performance_bar_allowed_group_path ApplicationSettings#performance_bar_allowed_group_path}
        :param personal_access_token_prefix: Prefix for all generated personal access tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#personal_access_token_prefix ApplicationSettings#personal_access_token_prefix}
        :param pipeline_limit_per_project_user_sha: Maximum number of pipeline creation requests per minute per user and commit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#pipeline_limit_per_project_user_sha ApplicationSettings#pipeline_limit_per_project_user_sha}
        :param plantuml_enabled: (If enabled, requires: plantuml_url) Enable PlantUML integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#plantuml_enabled ApplicationSettings#plantuml_enabled}
        :param plantuml_url: The PlantUML instance URL for integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#plantuml_url ApplicationSettings#plantuml_url}
        :param polling_interval_multiplier: Interval multiplier used by endpoints that perform polling. Set to 0 to disable polling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#polling_interval_multiplier ApplicationSettings#polling_interval_multiplier}
        :param project_export_enabled: Enable project export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#project_export_enabled ApplicationSettings#project_export_enabled}
        :param prometheus_metrics_enabled: Enable Prometheus metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#prometheus_metrics_enabled ApplicationSettings#prometheus_metrics_enabled}
        :param protected_ci_variables: CI/CD variables are protected by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#protected_ci_variables ApplicationSettings#protected_ci_variables}
        :param push_event_activities_limit: Number of changes (branches or tags) in a single push to determine whether individual push events or bulk push events are created. Bulk push events are created if it surpasses that value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#push_event_activities_limit ApplicationSettings#push_event_activities_limit}
        :param push_event_hooks_limit: Number of changes (branches or tags) in a single push to determine whether webhooks and services fire or not. Webhooks and services aren’t submitted if it surpasses that value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#push_event_hooks_limit ApplicationSettings#push_event_hooks_limit}
        :param pypi_package_requests_forwarding: Use pypi.org as a default remote repository when the package is not found in the GitLab Package Registry for PyPI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#pypi_package_requests_forwarding ApplicationSettings#pypi_package_requests_forwarding}
        :param rate_limiting_response_text: When rate limiting is enabled via the throttle_* settings, send this plain text response when a rate limit is exceeded. ‘Retry later’ is sent if this is blank. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#rate_limiting_response_text ApplicationSettings#rate_limiting_response_text}
        :param raw_blob_request_limit: Max number of requests per minute for each raw path. To disable throttling set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#raw_blob_request_limit ApplicationSettings#raw_blob_request_limit}
        :param recaptcha_enabled: (If enabled, requires: recaptcha_private_key and recaptcha_site_key) Enable reCAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#recaptcha_enabled ApplicationSettings#recaptcha_enabled}
        :param recaptcha_private_key: Private key for reCAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#recaptcha_private_key ApplicationSettings#recaptcha_private_key}
        :param recaptcha_site_key: Site key for reCAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#recaptcha_site_key ApplicationSettings#recaptcha_site_key}
        :param receive_max_input_size: Maximum push size (MB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#receive_max_input_size ApplicationSettings#receive_max_input_size}
        :param repository_checks_enabled: GitLab periodically runs git fsck in all project and wiki repositories to look for silent disk corruption issues. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_checks_enabled ApplicationSettings#repository_checks_enabled}
        :param repository_size_limit: Size limit per repository (MB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_size_limit ApplicationSettings#repository_size_limit}
        :param repository_storages: (GitLab 13.0 and earlier) List of names of enabled storage paths, taken from gitlab.yml. New projects are created in one of these stores, chosen at random. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_storages ApplicationSettings#repository_storages}
        :param repository_storages_weighted: (GitLab 13.1 and later) Hash of names of taken from gitlab.yml to weights. New projects are created in one of these stores, chosen by a weighted random selection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_storages_weighted ApplicationSettings#repository_storages_weighted}
        :param require_admin_approval_after_user_signup: When enabled, any user that signs up for an account using the registration form is placed under a Pending approval state and has to be explicitly approved by an administrator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#require_admin_approval_after_user_signup ApplicationSettings#require_admin_approval_after_user_signup}
        :param require_two_factor_authentication: (If enabled, requires: two_factor_grace_period) Require all users to set up Two-factor authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#require_two_factor_authentication ApplicationSettings#require_two_factor_authentication}
        :param restricted_visibility_levels: Selected levels cannot be used by non-Administrator users for groups, projects or snippets. Can take private, internal and public as a parameter. Null means there is no restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#restricted_visibility_levels ApplicationSettings#restricted_visibility_levels}
        :param rsa_key_restriction: The minimum allowed bit length of an uploaded RSA key. 0 means no restriction. -1 disables RSA keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#rsa_key_restriction ApplicationSettings#rsa_key_restriction}
        :param search_rate_limit: Max number of requests per minute for performing a search while authenticated. To disable throttling set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#search_rate_limit ApplicationSettings#search_rate_limit}
        :param search_rate_limit_unauthenticated: Max number of requests per minute for performing a search while unauthenticated. To disable throttling set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#search_rate_limit_unauthenticated ApplicationSettings#search_rate_limit_unauthenticated}
        :param send_user_confirmation_email: Send confirmation email on sign-up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#send_user_confirmation_email ApplicationSettings#send_user_confirmation_email}
        :param session_expire_delay: Session duration in minutes. GitLab restart is required to apply changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#session_expire_delay ApplicationSettings#session_expire_delay}
        :param shared_runners_enabled: (If enabled, requires: shared_runners_text and shared_runners_minutes) Enable shared runners for new projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#shared_runners_enabled ApplicationSettings#shared_runners_enabled}
        :param shared_runners_minutes: Set the maximum number of CI/CD minutes that a group can use on shared runners per month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#shared_runners_minutes ApplicationSettings#shared_runners_minutes}
        :param shared_runners_text: Shared runners text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#shared_runners_text ApplicationSettings#shared_runners_text}
        :param sidekiq_job_limiter_compression_threshold_bytes: The threshold in bytes at which Sidekiq jobs are compressed before being stored in Redis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sidekiq_job_limiter_compression_threshold_bytes ApplicationSettings#sidekiq_job_limiter_compression_threshold_bytes}
        :param sidekiq_job_limiter_limit_bytes: The threshold in bytes at which Sidekiq jobs are rejected. 0 means do not reject any job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sidekiq_job_limiter_limit_bytes ApplicationSettings#sidekiq_job_limiter_limit_bytes}
        :param sidekiq_job_limiter_mode: track or compress. Sets the behavior for Sidekiq job size limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sidekiq_job_limiter_mode ApplicationSettings#sidekiq_job_limiter_mode}
        :param sign_in_text: Text on the login page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sign_in_text ApplicationSettings#sign_in_text}
        :param signup_enabled: Enable registration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#signup_enabled ApplicationSettings#signup_enabled}
        :param slack_app_enabled: (If enabled, requires: slack_app_id, slack_app_secret and slack_app_secret) Enable Slack app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_enabled ApplicationSettings#slack_app_enabled}
        :param slack_app_id: The app ID of the Slack-app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_id ApplicationSettings#slack_app_id}
        :param slack_app_secret: The app secret of the Slack-app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_secret ApplicationSettings#slack_app_secret}
        :param slack_app_signing_secret: The signing secret of the Slack-app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_signing_secret ApplicationSettings#slack_app_signing_secret}
        :param slack_app_verification_token: The verification token of the Slack-app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_verification_token ApplicationSettings#slack_app_verification_token}
        :param snippet_size_limit: Max snippet content size in bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snippet_size_limit ApplicationSettings#snippet_size_limit}
        :param snowplow_app_id: The Snowplow site name / application ID. (for example, gitlab). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_app_id ApplicationSettings#snowplow_app_id}
        :param snowplow_collector_hostname: The Snowplow collector hostname. (for example, snowplow.trx.gitlab.net). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_collector_hostname ApplicationSettings#snowplow_collector_hostname}
        :param snowplow_cookie_domain: The Snowplow cookie domain. (for example, .gitlab.com). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_cookie_domain ApplicationSettings#snowplow_cookie_domain}
        :param snowplow_enabled: Enable snowplow tracking. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_enabled ApplicationSettings#snowplow_enabled}
        :param sourcegraph_enabled: Enables Sourcegraph integration. If enabled, requires sourcegraph_url. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sourcegraph_enabled ApplicationSettings#sourcegraph_enabled}
        :param sourcegraph_public_only: Blocks Sourcegraph from being loaded on private and internal projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sourcegraph_public_only ApplicationSettings#sourcegraph_public_only}
        :param sourcegraph_url: The Sourcegraph instance URL for integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sourcegraph_url ApplicationSettings#sourcegraph_url}
        :param spam_check_api_key: API key used by GitLab for accessing the Spam Check service endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#spam_check_api_key ApplicationSettings#spam_check_api_key}
        :param spam_check_endpoint_enabled: Enables spam checking using external Spam Check API endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#spam_check_endpoint_enabled ApplicationSettings#spam_check_endpoint_enabled}
        :param spam_check_endpoint_url: URL of the external Spamcheck service endpoint. Valid URI schemes are grpc or tls. Specifying tls forces communication to be encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#spam_check_endpoint_url ApplicationSettings#spam_check_endpoint_url}
        :param suggest_pipeline_enabled: Enable pipeline suggestion banner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#suggest_pipeline_enabled ApplicationSettings#suggest_pipeline_enabled}
        :param terminal_max_session_time: Maximum time for web terminal websocket connection (in seconds). Set to 0 for unlimited time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#terminal_max_session_time ApplicationSettings#terminal_max_session_time}
        :param terms: (Required by: enforce_terms) Markdown content for the ToS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#terms ApplicationSettings#terms}
        :param throttle_authenticated_api_enabled: (If enabled, requires: throttle_authenticated_api_period_in_seconds and throttle_authenticated_api_requests_per_period) Enable authenticated API request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_api_enabled ApplicationSettings#throttle_authenticated_api_enabled}
        :param throttle_authenticated_api_period_in_seconds: Rate limit period (in seconds). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_api_period_in_seconds ApplicationSettings#throttle_authenticated_api_period_in_seconds}
        :param throttle_authenticated_api_requests_per_period: Maximum requests per period per user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_api_requests_per_period ApplicationSettings#throttle_authenticated_api_requests_per_period}
        :param throttle_authenticated_packages_api_enabled: (If enabled, requires: throttle_authenticated_packages_api_period_in_seconds and throttle_authenticated_packages_api_requests_per_period) Enable authenticated API request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_packages_api_enabled ApplicationSettings#throttle_authenticated_packages_api_enabled}
        :param throttle_authenticated_packages_api_period_in_seconds: Rate limit period (in seconds). View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_packages_api_period_in_seconds ApplicationSettings#throttle_authenticated_packages_api_period_in_seconds}
        :param throttle_authenticated_packages_api_requests_per_period: Maximum requests per period per user. View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_packages_api_requests_per_period ApplicationSettings#throttle_authenticated_packages_api_requests_per_period}
        :param throttle_authenticated_web_enabled: (If enabled, requires: throttle_authenticated_web_period_in_seconds and throttle_authenticated_web_requests_per_period) Enable authenticated web request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_web_enabled ApplicationSettings#throttle_authenticated_web_enabled}
        :param throttle_authenticated_web_period_in_seconds: Rate limit period (in seconds). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_web_period_in_seconds ApplicationSettings#throttle_authenticated_web_period_in_seconds}
        :param throttle_authenticated_web_requests_per_period: Maximum requests per period per user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_web_requests_per_period ApplicationSettings#throttle_authenticated_web_requests_per_period}
        :param throttle_unauthenticated_api_enabled: (If enabled, requires: throttle_unauthenticated_api_period_in_seconds and throttle_unauthenticated_api_requests_per_period) Enable unauthenticated API request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_api_enabled ApplicationSettings#throttle_unauthenticated_api_enabled}
        :param throttle_unauthenticated_api_period_in_seconds: Rate limit period in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_api_period_in_seconds ApplicationSettings#throttle_unauthenticated_api_period_in_seconds}
        :param throttle_unauthenticated_api_requests_per_period: Max requests per period per IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_api_requests_per_period ApplicationSettings#throttle_unauthenticated_api_requests_per_period}
        :param throttle_unauthenticated_packages_api_enabled: (If enabled, requires: throttle_unauthenticated_packages_api_period_in_seconds and throttle_unauthenticated_packages_api_requests_per_period) Enable authenticated API request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_packages_api_enabled ApplicationSettings#throttle_unauthenticated_packages_api_enabled}
        :param throttle_unauthenticated_packages_api_period_in_seconds: Rate limit period (in seconds). View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_packages_api_period_in_seconds ApplicationSettings#throttle_unauthenticated_packages_api_period_in_seconds}
        :param throttle_unauthenticated_packages_api_requests_per_period: Maximum requests per period per user. View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_packages_api_requests_per_period ApplicationSettings#throttle_unauthenticated_packages_api_requests_per_period}
        :param throttle_unauthenticated_web_enabled: (If enabled, requires: throttle_unauthenticated_web_period_in_seconds and throttle_unauthenticated_web_requests_per_period) Enable unauthenticated web request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_web_enabled ApplicationSettings#throttle_unauthenticated_web_enabled}
        :param throttle_unauthenticated_web_period_in_seconds: Rate limit period in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_web_period_in_seconds ApplicationSettings#throttle_unauthenticated_web_period_in_seconds}
        :param throttle_unauthenticated_web_requests_per_period: Max requests per period per IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_web_requests_per_period ApplicationSettings#throttle_unauthenticated_web_requests_per_period}
        :param time_tracking_limit_to_hours: Limit display of time tracking units to hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#time_tracking_limit_to_hours ApplicationSettings#time_tracking_limit_to_hours}
        :param two_factor_grace_period: Amount of time (in hours) that users are allowed to skip forced configuration of two-factor authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#two_factor_grace_period ApplicationSettings#two_factor_grace_period}
        :param unique_ips_limit_enabled: (If enabled, requires: unique_ips_limit_per_user and unique_ips_limit_time_window) Limit sign in from multiple IPs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#unique_ips_limit_enabled ApplicationSettings#unique_ips_limit_enabled}
        :param unique_ips_limit_per_user: Maximum number of IPs per user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#unique_ips_limit_per_user ApplicationSettings#unique_ips_limit_per_user}
        :param unique_ips_limit_time_window: How many seconds an IP is counted towards the limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#unique_ips_limit_time_window ApplicationSettings#unique_ips_limit_time_window}
        :param usage_ping_enabled: Every week GitLab reports license usage back to GitLab, Inc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#usage_ping_enabled ApplicationSettings#usage_ping_enabled}
        :param user_deactivation_emails_enabled: Send an email to users upon account deactivation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_deactivation_emails_enabled ApplicationSettings#user_deactivation_emails_enabled}
        :param user_default_external: Newly registered users are external by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_default_external ApplicationSettings#user_default_external}
        :param user_default_internal_regex: Specify an email address regex pattern to identify default internal users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_default_internal_regex ApplicationSettings#user_default_internal_regex}
        :param user_oauth_applications: Allow users to register any application to use GitLab as an OAuth provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_oauth_applications ApplicationSettings#user_oauth_applications}
        :param user_show_add_ssh_key_message: When set to false disable the You won't be able to pull or push project code via SSH warning shown to users with no uploaded SSH key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_show_add_ssh_key_message ApplicationSettings#user_show_add_ssh_key_message}
        :param version_check_enabled: Let GitLab inform you when an update is available. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#version_check_enabled ApplicationSettings#version_check_enabled}
        :param web_ide_clientside_preview_enabled: Live Preview (allow live previews of JavaScript projects in the Web IDE using CodeSandbox Live Preview). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#web_ide_clientside_preview_enabled ApplicationSettings#web_ide_clientside_preview_enabled}
        :param whats_new_variant: What’s new variant, possible values: all_tiers, current_tier, and disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#whats_new_variant ApplicationSettings#whats_new_variant}
        :param wiki_page_max_content_bytes: Maximum wiki page content size in bytes. The minimum value is 1024 bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#wiki_page_max_content_bytes ApplicationSettings#wiki_page_max_content_bytes}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d3980c04bd791033464f1f44824149396aeebc0afa75a6dc4f6952627d2859)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApplicationSettingsConfig(
            abuse_notification_email=abuse_notification_email,
            admin_mode=admin_mode,
            after_sign_out_path=after_sign_out_path,
            after_sign_up_text=after_sign_up_text,
            akismet_api_key=akismet_api_key,
            akismet_enabled=akismet_enabled,
            allow_group_owners_to_manage_ldap=allow_group_owners_to_manage_ldap,
            allow_local_requests_from_system_hooks=allow_local_requests_from_system_hooks,
            allow_local_requests_from_web_hooks_and_services=allow_local_requests_from_web_hooks_and_services,
            archive_builds_in_human_readable=archive_builds_in_human_readable,
            asset_proxy_allowlist=asset_proxy_allowlist,
            asset_proxy_enabled=asset_proxy_enabled,
            asset_proxy_secret_key=asset_proxy_secret_key,
            asset_proxy_url=asset_proxy_url,
            authorized_keys_enabled=authorized_keys_enabled,
            auto_devops_domain=auto_devops_domain,
            auto_devops_enabled=auto_devops_enabled,
            automatic_purchased_storage_allocation=automatic_purchased_storage_allocation,
            can_create_group=can_create_group,
            check_namespace_plan=check_namespace_plan,
            commit_email_hostname=commit_email_hostname,
            container_expiration_policies_enable_historic_entries=container_expiration_policies_enable_historic_entries,
            container_registry_cleanup_tags_service_max_list_size=container_registry_cleanup_tags_service_max_list_size,
            container_registry_delete_tags_service_timeout=container_registry_delete_tags_service_timeout,
            container_registry_expiration_policies_caching=container_registry_expiration_policies_caching,
            container_registry_expiration_policies_worker_capacity=container_registry_expiration_policies_worker_capacity,
            container_registry_token_expire_delay=container_registry_token_expire_delay,
            deactivate_dormant_users=deactivate_dormant_users,
            default_artifacts_expire_in=default_artifacts_expire_in,
            default_branch_name=default_branch_name,
            default_branch_protection=default_branch_protection,
            default_ci_config_path=default_ci_config_path,
            default_group_visibility=default_group_visibility,
            default_project_creation=default_project_creation,
            default_projects_limit=default_projects_limit,
            default_project_visibility=default_project_visibility,
            default_snippet_visibility=default_snippet_visibility,
            delayed_group_deletion=delayed_group_deletion,
            delayed_project_deletion=delayed_project_deletion,
            delete_inactive_projects=delete_inactive_projects,
            deletion_adjourned_period=deletion_adjourned_period,
            diff_max_files=diff_max_files,
            diff_max_lines=diff_max_lines,
            diff_max_patch_bytes=diff_max_patch_bytes,
            disabled_oauth_sign_in_sources=disabled_oauth_sign_in_sources,
            disable_feed_token=disable_feed_token,
            dns_rebinding_protection_enabled=dns_rebinding_protection_enabled,
            domain_allowlist=domain_allowlist,
            domain_denylist=domain_denylist,
            domain_denylist_enabled=domain_denylist_enabled,
            dsa_key_restriction=dsa_key_restriction,
            ecdsa_key_restriction=ecdsa_key_restriction,
            ecdsa_sk_key_restriction=ecdsa_sk_key_restriction,
            ed25519_key_restriction=ed25519_key_restriction,
            ed25519_sk_key_restriction=ed25519_sk_key_restriction,
            eks_access_key_id=eks_access_key_id,
            eks_account_id=eks_account_id,
            eks_integration_enabled=eks_integration_enabled,
            eks_secret_access_key=eks_secret_access_key,
            elasticsearch_aws=elasticsearch_aws,
            elasticsearch_aws_access_key=elasticsearch_aws_access_key,
            elasticsearch_aws_region=elasticsearch_aws_region,
            elasticsearch_aws_secret_access_key=elasticsearch_aws_secret_access_key,
            elasticsearch_indexed_field_length_limit=elasticsearch_indexed_field_length_limit,
            elasticsearch_indexed_file_size_limit_kb=elasticsearch_indexed_file_size_limit_kb,
            elasticsearch_indexing=elasticsearch_indexing,
            elasticsearch_limit_indexing=elasticsearch_limit_indexing,
            elasticsearch_max_bulk_concurrency=elasticsearch_max_bulk_concurrency,
            elasticsearch_max_bulk_size_mb=elasticsearch_max_bulk_size_mb,
            elasticsearch_namespace_ids=elasticsearch_namespace_ids,
            elasticsearch_password=elasticsearch_password,
            elasticsearch_project_ids=elasticsearch_project_ids,
            elasticsearch_search=elasticsearch_search,
            elasticsearch_url=elasticsearch_url,
            elasticsearch_username=elasticsearch_username,
            email_additional_text=email_additional_text,
            email_author_in_body=email_author_in_body,
            enabled_git_access_protocol=enabled_git_access_protocol,
            enforce_namespace_storage_limit=enforce_namespace_storage_limit,
            enforce_terms=enforce_terms,
            external_auth_client_cert=external_auth_client_cert,
            external_auth_client_key=external_auth_client_key,
            external_auth_client_key_pass=external_auth_client_key_pass,
            external_authorization_service_default_label=external_authorization_service_default_label,
            external_authorization_service_enabled=external_authorization_service_enabled,
            external_authorization_service_timeout=external_authorization_service_timeout,
            external_authorization_service_url=external_authorization_service_url,
            external_pipeline_validation_service_timeout=external_pipeline_validation_service_timeout,
            external_pipeline_validation_service_token=external_pipeline_validation_service_token,
            external_pipeline_validation_service_url=external_pipeline_validation_service_url,
            file_template_project_id=file_template_project_id,
            first_day_of_week=first_day_of_week,
            geo_node_allowed_ips=geo_node_allowed_ips,
            geo_status_timeout=geo_status_timeout,
            gitaly_timeout_default=gitaly_timeout_default,
            gitaly_timeout_fast=gitaly_timeout_fast,
            gitaly_timeout_medium=gitaly_timeout_medium,
            git_rate_limit_users_allowlist=git_rate_limit_users_allowlist,
            git_two_factor_session_expiry=git_two_factor_session_expiry,
            grafana_enabled=grafana_enabled,
            grafana_url=grafana_url,
            gravatar_enabled=gravatar_enabled,
            group_owners_can_manage_default_branch_protection=group_owners_can_manage_default_branch_protection,
            hashed_storage_enabled=hashed_storage_enabled,
            help_page_hide_commercial_content=help_page_hide_commercial_content,
            help_page_support_url=help_page_support_url,
            help_page_text=help_page_text,
            help_text=help_text,
            hide_third_party_offers=hide_third_party_offers,
            home_page_url=home_page_url,
            housekeeping_enabled=housekeeping_enabled,
            housekeeping_full_repack_period=housekeeping_full_repack_period,
            housekeeping_gc_period=housekeeping_gc_period,
            housekeeping_incremental_repack_period=housekeeping_incremental_repack_period,
            html_emails_enabled=html_emails_enabled,
            id=id,
            import_sources=import_sources,
            inactive_projects_delete_after_months=inactive_projects_delete_after_months,
            inactive_projects_min_size_mb=inactive_projects_min_size_mb,
            inactive_projects_send_warning_email_after_months=inactive_projects_send_warning_email_after_months,
            in_product_marketing_emails_enabled=in_product_marketing_emails_enabled,
            invisible_captcha_enabled=invisible_captcha_enabled,
            issues_create_limit=issues_create_limit,
            keep_latest_artifact=keep_latest_artifact,
            local_markdown_version=local_markdown_version,
            mailgun_events_enabled=mailgun_events_enabled,
            mailgun_signing_key=mailgun_signing_key,
            maintenance_mode=maintenance_mode,
            maintenance_mode_message=maintenance_mode_message,
            max_artifacts_size=max_artifacts_size,
            max_attachment_size=max_attachment_size,
            max_export_size=max_export_size,
            max_import_size=max_import_size,
            max_number_of_repository_downloads=max_number_of_repository_downloads,
            max_number_of_repository_downloads_within_time_period=max_number_of_repository_downloads_within_time_period,
            max_pages_size=max_pages_size,
            max_personal_access_token_lifetime=max_personal_access_token_lifetime,
            max_ssh_key_lifetime=max_ssh_key_lifetime,
            metrics_method_call_threshold=metrics_method_call_threshold,
            mirror_available=mirror_available,
            mirror_capacity_threshold=mirror_capacity_threshold,
            mirror_max_capacity=mirror_max_capacity,
            mirror_max_delay=mirror_max_delay,
            npm_package_requests_forwarding=npm_package_requests_forwarding,
            outbound_local_requests_whitelist=outbound_local_requests_whitelist,
            package_registry_cleanup_policies_worker_capacity=package_registry_cleanup_policies_worker_capacity,
            pages_domain_verification_enabled=pages_domain_verification_enabled,
            password_authentication_enabled_for_git=password_authentication_enabled_for_git,
            password_authentication_enabled_for_web=password_authentication_enabled_for_web,
            password_lowercase_required=password_lowercase_required,
            password_number_required=password_number_required,
            password_symbol_required=password_symbol_required,
            password_uppercase_required=password_uppercase_required,
            performance_bar_allowed_group_path=performance_bar_allowed_group_path,
            personal_access_token_prefix=personal_access_token_prefix,
            pipeline_limit_per_project_user_sha=pipeline_limit_per_project_user_sha,
            plantuml_enabled=plantuml_enabled,
            plantuml_url=plantuml_url,
            polling_interval_multiplier=polling_interval_multiplier,
            project_export_enabled=project_export_enabled,
            prometheus_metrics_enabled=prometheus_metrics_enabled,
            protected_ci_variables=protected_ci_variables,
            push_event_activities_limit=push_event_activities_limit,
            push_event_hooks_limit=push_event_hooks_limit,
            pypi_package_requests_forwarding=pypi_package_requests_forwarding,
            rate_limiting_response_text=rate_limiting_response_text,
            raw_blob_request_limit=raw_blob_request_limit,
            recaptcha_enabled=recaptcha_enabled,
            recaptcha_private_key=recaptcha_private_key,
            recaptcha_site_key=recaptcha_site_key,
            receive_max_input_size=receive_max_input_size,
            repository_checks_enabled=repository_checks_enabled,
            repository_size_limit=repository_size_limit,
            repository_storages=repository_storages,
            repository_storages_weighted=repository_storages_weighted,
            require_admin_approval_after_user_signup=require_admin_approval_after_user_signup,
            require_two_factor_authentication=require_two_factor_authentication,
            restricted_visibility_levels=restricted_visibility_levels,
            rsa_key_restriction=rsa_key_restriction,
            search_rate_limit=search_rate_limit,
            search_rate_limit_unauthenticated=search_rate_limit_unauthenticated,
            send_user_confirmation_email=send_user_confirmation_email,
            session_expire_delay=session_expire_delay,
            shared_runners_enabled=shared_runners_enabled,
            shared_runners_minutes=shared_runners_minutes,
            shared_runners_text=shared_runners_text,
            sidekiq_job_limiter_compression_threshold_bytes=sidekiq_job_limiter_compression_threshold_bytes,
            sidekiq_job_limiter_limit_bytes=sidekiq_job_limiter_limit_bytes,
            sidekiq_job_limiter_mode=sidekiq_job_limiter_mode,
            sign_in_text=sign_in_text,
            signup_enabled=signup_enabled,
            slack_app_enabled=slack_app_enabled,
            slack_app_id=slack_app_id,
            slack_app_secret=slack_app_secret,
            slack_app_signing_secret=slack_app_signing_secret,
            slack_app_verification_token=slack_app_verification_token,
            snippet_size_limit=snippet_size_limit,
            snowplow_app_id=snowplow_app_id,
            snowplow_collector_hostname=snowplow_collector_hostname,
            snowplow_cookie_domain=snowplow_cookie_domain,
            snowplow_enabled=snowplow_enabled,
            sourcegraph_enabled=sourcegraph_enabled,
            sourcegraph_public_only=sourcegraph_public_only,
            sourcegraph_url=sourcegraph_url,
            spam_check_api_key=spam_check_api_key,
            spam_check_endpoint_enabled=spam_check_endpoint_enabled,
            spam_check_endpoint_url=spam_check_endpoint_url,
            suggest_pipeline_enabled=suggest_pipeline_enabled,
            terminal_max_session_time=terminal_max_session_time,
            terms=terms,
            throttle_authenticated_api_enabled=throttle_authenticated_api_enabled,
            throttle_authenticated_api_period_in_seconds=throttle_authenticated_api_period_in_seconds,
            throttle_authenticated_api_requests_per_period=throttle_authenticated_api_requests_per_period,
            throttle_authenticated_packages_api_enabled=throttle_authenticated_packages_api_enabled,
            throttle_authenticated_packages_api_period_in_seconds=throttle_authenticated_packages_api_period_in_seconds,
            throttle_authenticated_packages_api_requests_per_period=throttle_authenticated_packages_api_requests_per_period,
            throttle_authenticated_web_enabled=throttle_authenticated_web_enabled,
            throttle_authenticated_web_period_in_seconds=throttle_authenticated_web_period_in_seconds,
            throttle_authenticated_web_requests_per_period=throttle_authenticated_web_requests_per_period,
            throttle_unauthenticated_api_enabled=throttle_unauthenticated_api_enabled,
            throttle_unauthenticated_api_period_in_seconds=throttle_unauthenticated_api_period_in_seconds,
            throttle_unauthenticated_api_requests_per_period=throttle_unauthenticated_api_requests_per_period,
            throttle_unauthenticated_packages_api_enabled=throttle_unauthenticated_packages_api_enabled,
            throttle_unauthenticated_packages_api_period_in_seconds=throttle_unauthenticated_packages_api_period_in_seconds,
            throttle_unauthenticated_packages_api_requests_per_period=throttle_unauthenticated_packages_api_requests_per_period,
            throttle_unauthenticated_web_enabled=throttle_unauthenticated_web_enabled,
            throttle_unauthenticated_web_period_in_seconds=throttle_unauthenticated_web_period_in_seconds,
            throttle_unauthenticated_web_requests_per_period=throttle_unauthenticated_web_requests_per_period,
            time_tracking_limit_to_hours=time_tracking_limit_to_hours,
            two_factor_grace_period=two_factor_grace_period,
            unique_ips_limit_enabled=unique_ips_limit_enabled,
            unique_ips_limit_per_user=unique_ips_limit_per_user,
            unique_ips_limit_time_window=unique_ips_limit_time_window,
            usage_ping_enabled=usage_ping_enabled,
            user_deactivation_emails_enabled=user_deactivation_emails_enabled,
            user_default_external=user_default_external,
            user_default_internal_regex=user_default_internal_regex,
            user_oauth_applications=user_oauth_applications,
            user_show_add_ssh_key_message=user_show_add_ssh_key_message,
            version_check_enabled=version_check_enabled,
            web_ide_clientside_preview_enabled=web_ide_clientside_preview_enabled,
            whats_new_variant=whats_new_variant,
            wiki_page_max_content_bytes=wiki_page_max_content_bytes,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAbuseNotificationEmail")
    def reset_abuse_notification_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAbuseNotificationEmail", []))

    @jsii.member(jsii_name="resetAdminMode")
    def reset_admin_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminMode", []))

    @jsii.member(jsii_name="resetAfterSignOutPath")
    def reset_after_sign_out_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAfterSignOutPath", []))

    @jsii.member(jsii_name="resetAfterSignUpText")
    def reset_after_sign_up_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAfterSignUpText", []))

    @jsii.member(jsii_name="resetAkismetApiKey")
    def reset_akismet_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAkismetApiKey", []))

    @jsii.member(jsii_name="resetAkismetEnabled")
    def reset_akismet_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAkismetEnabled", []))

    @jsii.member(jsii_name="resetAllowGroupOwnersToManageLdap")
    def reset_allow_group_owners_to_manage_ldap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowGroupOwnersToManageLdap", []))

    @jsii.member(jsii_name="resetAllowLocalRequestsFromSystemHooks")
    def reset_allow_local_requests_from_system_hooks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowLocalRequestsFromSystemHooks", []))

    @jsii.member(jsii_name="resetAllowLocalRequestsFromWebHooksAndServices")
    def reset_allow_local_requests_from_web_hooks_and_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowLocalRequestsFromWebHooksAndServices", []))

    @jsii.member(jsii_name="resetArchiveBuildsInHumanReadable")
    def reset_archive_builds_in_human_readable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveBuildsInHumanReadable", []))

    @jsii.member(jsii_name="resetAssetProxyAllowlist")
    def reset_asset_proxy_allowlist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetProxyAllowlist", []))

    @jsii.member(jsii_name="resetAssetProxyEnabled")
    def reset_asset_proxy_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetProxyEnabled", []))

    @jsii.member(jsii_name="resetAssetProxySecretKey")
    def reset_asset_proxy_secret_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetProxySecretKey", []))

    @jsii.member(jsii_name="resetAssetProxyUrl")
    def reset_asset_proxy_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssetProxyUrl", []))

    @jsii.member(jsii_name="resetAuthorizedKeysEnabled")
    def reset_authorized_keys_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizedKeysEnabled", []))

    @jsii.member(jsii_name="resetAutoDevopsDomain")
    def reset_auto_devops_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDevopsDomain", []))

    @jsii.member(jsii_name="resetAutoDevopsEnabled")
    def reset_auto_devops_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoDevopsEnabled", []))

    @jsii.member(jsii_name="resetAutomaticPurchasedStorageAllocation")
    def reset_automatic_purchased_storage_allocation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticPurchasedStorageAllocation", []))

    @jsii.member(jsii_name="resetCanCreateGroup")
    def reset_can_create_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanCreateGroup", []))

    @jsii.member(jsii_name="resetCheckNamespacePlan")
    def reset_check_namespace_plan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckNamespacePlan", []))

    @jsii.member(jsii_name="resetCommitEmailHostname")
    def reset_commit_email_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommitEmailHostname", []))

    @jsii.member(jsii_name="resetContainerExpirationPoliciesEnableHistoricEntries")
    def reset_container_expiration_policies_enable_historic_entries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerExpirationPoliciesEnableHistoricEntries", []))

    @jsii.member(jsii_name="resetContainerRegistryCleanupTagsServiceMaxListSize")
    def reset_container_registry_cleanup_tags_service_max_list_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistryCleanupTagsServiceMaxListSize", []))

    @jsii.member(jsii_name="resetContainerRegistryDeleteTagsServiceTimeout")
    def reset_container_registry_delete_tags_service_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistryDeleteTagsServiceTimeout", []))

    @jsii.member(jsii_name="resetContainerRegistryExpirationPoliciesCaching")
    def reset_container_registry_expiration_policies_caching(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistryExpirationPoliciesCaching", []))

    @jsii.member(jsii_name="resetContainerRegistryExpirationPoliciesWorkerCapacity")
    def reset_container_registry_expiration_policies_worker_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistryExpirationPoliciesWorkerCapacity", []))

    @jsii.member(jsii_name="resetContainerRegistryTokenExpireDelay")
    def reset_container_registry_token_expire_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistryTokenExpireDelay", []))

    @jsii.member(jsii_name="resetDeactivateDormantUsers")
    def reset_deactivate_dormant_users(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeactivateDormantUsers", []))

    @jsii.member(jsii_name="resetDefaultArtifactsExpireIn")
    def reset_default_artifacts_expire_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultArtifactsExpireIn", []))

    @jsii.member(jsii_name="resetDefaultBranchName")
    def reset_default_branch_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBranchName", []))

    @jsii.member(jsii_name="resetDefaultBranchProtection")
    def reset_default_branch_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBranchProtection", []))

    @jsii.member(jsii_name="resetDefaultCiConfigPath")
    def reset_default_ci_config_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultCiConfigPath", []))

    @jsii.member(jsii_name="resetDefaultGroupVisibility")
    def reset_default_group_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultGroupVisibility", []))

    @jsii.member(jsii_name="resetDefaultProjectCreation")
    def reset_default_project_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultProjectCreation", []))

    @jsii.member(jsii_name="resetDefaultProjectsLimit")
    def reset_default_projects_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultProjectsLimit", []))

    @jsii.member(jsii_name="resetDefaultProjectVisibility")
    def reset_default_project_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultProjectVisibility", []))

    @jsii.member(jsii_name="resetDefaultSnippetVisibility")
    def reset_default_snippet_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultSnippetVisibility", []))

    @jsii.member(jsii_name="resetDelayedGroupDeletion")
    def reset_delayed_group_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelayedGroupDeletion", []))

    @jsii.member(jsii_name="resetDelayedProjectDeletion")
    def reset_delayed_project_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelayedProjectDeletion", []))

    @jsii.member(jsii_name="resetDeleteInactiveProjects")
    def reset_delete_inactive_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteInactiveProjects", []))

    @jsii.member(jsii_name="resetDeletionAdjournedPeriod")
    def reset_deletion_adjourned_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionAdjournedPeriod", []))

    @jsii.member(jsii_name="resetDiffMaxFiles")
    def reset_diff_max_files(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiffMaxFiles", []))

    @jsii.member(jsii_name="resetDiffMaxLines")
    def reset_diff_max_lines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiffMaxLines", []))

    @jsii.member(jsii_name="resetDiffMaxPatchBytes")
    def reset_diff_max_patch_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiffMaxPatchBytes", []))

    @jsii.member(jsii_name="resetDisabledOauthSignInSources")
    def reset_disabled_oauth_sign_in_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabledOauthSignInSources", []))

    @jsii.member(jsii_name="resetDisableFeedToken")
    def reset_disable_feed_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableFeedToken", []))

    @jsii.member(jsii_name="resetDnsRebindingProtectionEnabled")
    def reset_dns_rebinding_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsRebindingProtectionEnabled", []))

    @jsii.member(jsii_name="resetDomainAllowlist")
    def reset_domain_allowlist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainAllowlist", []))

    @jsii.member(jsii_name="resetDomainDenylist")
    def reset_domain_denylist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainDenylist", []))

    @jsii.member(jsii_name="resetDomainDenylistEnabled")
    def reset_domain_denylist_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainDenylistEnabled", []))

    @jsii.member(jsii_name="resetDsaKeyRestriction")
    def reset_dsa_key_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDsaKeyRestriction", []))

    @jsii.member(jsii_name="resetEcdsaKeyRestriction")
    def reset_ecdsa_key_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEcdsaKeyRestriction", []))

    @jsii.member(jsii_name="resetEcdsaSkKeyRestriction")
    def reset_ecdsa_sk_key_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEcdsaSkKeyRestriction", []))

    @jsii.member(jsii_name="resetEd25519KeyRestriction")
    def reset_ed25519_key_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEd25519KeyRestriction", []))

    @jsii.member(jsii_name="resetEd25519SkKeyRestriction")
    def reset_ed25519_sk_key_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEd25519SkKeyRestriction", []))

    @jsii.member(jsii_name="resetEksAccessKeyId")
    def reset_eks_access_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEksAccessKeyId", []))

    @jsii.member(jsii_name="resetEksAccountId")
    def reset_eks_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEksAccountId", []))

    @jsii.member(jsii_name="resetEksIntegrationEnabled")
    def reset_eks_integration_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEksIntegrationEnabled", []))

    @jsii.member(jsii_name="resetEksSecretAccessKey")
    def reset_eks_secret_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEksSecretAccessKey", []))

    @jsii.member(jsii_name="resetElasticsearchAws")
    def reset_elasticsearch_aws(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchAws", []))

    @jsii.member(jsii_name="resetElasticsearchAwsAccessKey")
    def reset_elasticsearch_aws_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchAwsAccessKey", []))

    @jsii.member(jsii_name="resetElasticsearchAwsRegion")
    def reset_elasticsearch_aws_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchAwsRegion", []))

    @jsii.member(jsii_name="resetElasticsearchAwsSecretAccessKey")
    def reset_elasticsearch_aws_secret_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchAwsSecretAccessKey", []))

    @jsii.member(jsii_name="resetElasticsearchIndexedFieldLengthLimit")
    def reset_elasticsearch_indexed_field_length_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchIndexedFieldLengthLimit", []))

    @jsii.member(jsii_name="resetElasticsearchIndexedFileSizeLimitKb")
    def reset_elasticsearch_indexed_file_size_limit_kb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchIndexedFileSizeLimitKb", []))

    @jsii.member(jsii_name="resetElasticsearchIndexing")
    def reset_elasticsearch_indexing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchIndexing", []))

    @jsii.member(jsii_name="resetElasticsearchLimitIndexing")
    def reset_elasticsearch_limit_indexing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchLimitIndexing", []))

    @jsii.member(jsii_name="resetElasticsearchMaxBulkConcurrency")
    def reset_elasticsearch_max_bulk_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchMaxBulkConcurrency", []))

    @jsii.member(jsii_name="resetElasticsearchMaxBulkSizeMb")
    def reset_elasticsearch_max_bulk_size_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchMaxBulkSizeMb", []))

    @jsii.member(jsii_name="resetElasticsearchNamespaceIds")
    def reset_elasticsearch_namespace_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchNamespaceIds", []))

    @jsii.member(jsii_name="resetElasticsearchPassword")
    def reset_elasticsearch_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchPassword", []))

    @jsii.member(jsii_name="resetElasticsearchProjectIds")
    def reset_elasticsearch_project_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchProjectIds", []))

    @jsii.member(jsii_name="resetElasticsearchSearch")
    def reset_elasticsearch_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchSearch", []))

    @jsii.member(jsii_name="resetElasticsearchUrl")
    def reset_elasticsearch_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchUrl", []))

    @jsii.member(jsii_name="resetElasticsearchUsername")
    def reset_elasticsearch_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchUsername", []))

    @jsii.member(jsii_name="resetEmailAdditionalText")
    def reset_email_additional_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAdditionalText", []))

    @jsii.member(jsii_name="resetEmailAuthorInBody")
    def reset_email_author_in_body(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAuthorInBody", []))

    @jsii.member(jsii_name="resetEnabledGitAccessProtocol")
    def reset_enabled_git_access_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabledGitAccessProtocol", []))

    @jsii.member(jsii_name="resetEnforceNamespaceStorageLimit")
    def reset_enforce_namespace_storage_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceNamespaceStorageLimit", []))

    @jsii.member(jsii_name="resetEnforceTerms")
    def reset_enforce_terms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceTerms", []))

    @jsii.member(jsii_name="resetExternalAuthClientCert")
    def reset_external_auth_client_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAuthClientCert", []))

    @jsii.member(jsii_name="resetExternalAuthClientKey")
    def reset_external_auth_client_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAuthClientKey", []))

    @jsii.member(jsii_name="resetExternalAuthClientKeyPass")
    def reset_external_auth_client_key_pass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAuthClientKeyPass", []))

    @jsii.member(jsii_name="resetExternalAuthorizationServiceDefaultLabel")
    def reset_external_authorization_service_default_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAuthorizationServiceDefaultLabel", []))

    @jsii.member(jsii_name="resetExternalAuthorizationServiceEnabled")
    def reset_external_authorization_service_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAuthorizationServiceEnabled", []))

    @jsii.member(jsii_name="resetExternalAuthorizationServiceTimeout")
    def reset_external_authorization_service_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAuthorizationServiceTimeout", []))

    @jsii.member(jsii_name="resetExternalAuthorizationServiceUrl")
    def reset_external_authorization_service_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAuthorizationServiceUrl", []))

    @jsii.member(jsii_name="resetExternalPipelineValidationServiceTimeout")
    def reset_external_pipeline_validation_service_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalPipelineValidationServiceTimeout", []))

    @jsii.member(jsii_name="resetExternalPipelineValidationServiceToken")
    def reset_external_pipeline_validation_service_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalPipelineValidationServiceToken", []))

    @jsii.member(jsii_name="resetExternalPipelineValidationServiceUrl")
    def reset_external_pipeline_validation_service_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalPipelineValidationServiceUrl", []))

    @jsii.member(jsii_name="resetFileTemplateProjectId")
    def reset_file_template_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileTemplateProjectId", []))

    @jsii.member(jsii_name="resetFirstDayOfWeek")
    def reset_first_day_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstDayOfWeek", []))

    @jsii.member(jsii_name="resetGeoNodeAllowedIps")
    def reset_geo_node_allowed_ips(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoNodeAllowedIps", []))

    @jsii.member(jsii_name="resetGeoStatusTimeout")
    def reset_geo_status_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoStatusTimeout", []))

    @jsii.member(jsii_name="resetGitalyTimeoutDefault")
    def reset_gitaly_timeout_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitalyTimeoutDefault", []))

    @jsii.member(jsii_name="resetGitalyTimeoutFast")
    def reset_gitaly_timeout_fast(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitalyTimeoutFast", []))

    @jsii.member(jsii_name="resetGitalyTimeoutMedium")
    def reset_gitaly_timeout_medium(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitalyTimeoutMedium", []))

    @jsii.member(jsii_name="resetGitRateLimitUsersAllowlist")
    def reset_git_rate_limit_users_allowlist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitRateLimitUsersAllowlist", []))

    @jsii.member(jsii_name="resetGitTwoFactorSessionExpiry")
    def reset_git_two_factor_session_expiry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitTwoFactorSessionExpiry", []))

    @jsii.member(jsii_name="resetGrafanaEnabled")
    def reset_grafana_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrafanaEnabled", []))

    @jsii.member(jsii_name="resetGrafanaUrl")
    def reset_grafana_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrafanaUrl", []))

    @jsii.member(jsii_name="resetGravatarEnabled")
    def reset_gravatar_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGravatarEnabled", []))

    @jsii.member(jsii_name="resetGroupOwnersCanManageDefaultBranchProtection")
    def reset_group_owners_can_manage_default_branch_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupOwnersCanManageDefaultBranchProtection", []))

    @jsii.member(jsii_name="resetHashedStorageEnabled")
    def reset_hashed_storage_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHashedStorageEnabled", []))

    @jsii.member(jsii_name="resetHelpPageHideCommercialContent")
    def reset_help_page_hide_commercial_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHelpPageHideCommercialContent", []))

    @jsii.member(jsii_name="resetHelpPageSupportUrl")
    def reset_help_page_support_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHelpPageSupportUrl", []))

    @jsii.member(jsii_name="resetHelpPageText")
    def reset_help_page_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHelpPageText", []))

    @jsii.member(jsii_name="resetHelpText")
    def reset_help_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHelpText", []))

    @jsii.member(jsii_name="resetHideThirdPartyOffers")
    def reset_hide_third_party_offers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHideThirdPartyOffers", []))

    @jsii.member(jsii_name="resetHomePageUrl")
    def reset_home_page_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHomePageUrl", []))

    @jsii.member(jsii_name="resetHousekeepingEnabled")
    def reset_housekeeping_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHousekeepingEnabled", []))

    @jsii.member(jsii_name="resetHousekeepingFullRepackPeriod")
    def reset_housekeeping_full_repack_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHousekeepingFullRepackPeriod", []))

    @jsii.member(jsii_name="resetHousekeepingGcPeriod")
    def reset_housekeeping_gc_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHousekeepingGcPeriod", []))

    @jsii.member(jsii_name="resetHousekeepingIncrementalRepackPeriod")
    def reset_housekeeping_incremental_repack_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHousekeepingIncrementalRepackPeriod", []))

    @jsii.member(jsii_name="resetHtmlEmailsEnabled")
    def reset_html_emails_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHtmlEmailsEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImportSources")
    def reset_import_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportSources", []))

    @jsii.member(jsii_name="resetInactiveProjectsDeleteAfterMonths")
    def reset_inactive_projects_delete_after_months(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInactiveProjectsDeleteAfterMonths", []))

    @jsii.member(jsii_name="resetInactiveProjectsMinSizeMb")
    def reset_inactive_projects_min_size_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInactiveProjectsMinSizeMb", []))

    @jsii.member(jsii_name="resetInactiveProjectsSendWarningEmailAfterMonths")
    def reset_inactive_projects_send_warning_email_after_months(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInactiveProjectsSendWarningEmailAfterMonths", []))

    @jsii.member(jsii_name="resetInProductMarketingEmailsEnabled")
    def reset_in_product_marketing_emails_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInProductMarketingEmailsEnabled", []))

    @jsii.member(jsii_name="resetInvisibleCaptchaEnabled")
    def reset_invisible_captcha_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvisibleCaptchaEnabled", []))

    @jsii.member(jsii_name="resetIssuesCreateLimit")
    def reset_issues_create_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuesCreateLimit", []))

    @jsii.member(jsii_name="resetKeepLatestArtifact")
    def reset_keep_latest_artifact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepLatestArtifact", []))

    @jsii.member(jsii_name="resetLocalMarkdownVersion")
    def reset_local_markdown_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalMarkdownVersion", []))

    @jsii.member(jsii_name="resetMailgunEventsEnabled")
    def reset_mailgun_events_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMailgunEventsEnabled", []))

    @jsii.member(jsii_name="resetMailgunSigningKey")
    def reset_mailgun_signing_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMailgunSigningKey", []))

    @jsii.member(jsii_name="resetMaintenanceMode")
    def reset_maintenance_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceMode", []))

    @jsii.member(jsii_name="resetMaintenanceModeMessage")
    def reset_maintenance_mode_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceModeMessage", []))

    @jsii.member(jsii_name="resetMaxArtifactsSize")
    def reset_max_artifacts_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxArtifactsSize", []))

    @jsii.member(jsii_name="resetMaxAttachmentSize")
    def reset_max_attachment_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAttachmentSize", []))

    @jsii.member(jsii_name="resetMaxExportSize")
    def reset_max_export_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxExportSize", []))

    @jsii.member(jsii_name="resetMaxImportSize")
    def reset_max_import_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxImportSize", []))

    @jsii.member(jsii_name="resetMaxNumberOfRepositoryDownloads")
    def reset_max_number_of_repository_downloads(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNumberOfRepositoryDownloads", []))

    @jsii.member(jsii_name="resetMaxNumberOfRepositoryDownloadsWithinTimePeriod")
    def reset_max_number_of_repository_downloads_within_time_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNumberOfRepositoryDownloadsWithinTimePeriod", []))

    @jsii.member(jsii_name="resetMaxPagesSize")
    def reset_max_pages_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPagesSize", []))

    @jsii.member(jsii_name="resetMaxPersonalAccessTokenLifetime")
    def reset_max_personal_access_token_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPersonalAccessTokenLifetime", []))

    @jsii.member(jsii_name="resetMaxSshKeyLifetime")
    def reset_max_ssh_key_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSshKeyLifetime", []))

    @jsii.member(jsii_name="resetMetricsMethodCallThreshold")
    def reset_metrics_method_call_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsMethodCallThreshold", []))

    @jsii.member(jsii_name="resetMirrorAvailable")
    def reset_mirror_available(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMirrorAvailable", []))

    @jsii.member(jsii_name="resetMirrorCapacityThreshold")
    def reset_mirror_capacity_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMirrorCapacityThreshold", []))

    @jsii.member(jsii_name="resetMirrorMaxCapacity")
    def reset_mirror_max_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMirrorMaxCapacity", []))

    @jsii.member(jsii_name="resetMirrorMaxDelay")
    def reset_mirror_max_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMirrorMaxDelay", []))

    @jsii.member(jsii_name="resetNpmPackageRequestsForwarding")
    def reset_npm_package_requests_forwarding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNpmPackageRequestsForwarding", []))

    @jsii.member(jsii_name="resetOutboundLocalRequestsWhitelist")
    def reset_outbound_local_requests_whitelist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundLocalRequestsWhitelist", []))

    @jsii.member(jsii_name="resetPackageRegistryCleanupPoliciesWorkerCapacity")
    def reset_package_registry_cleanup_policies_worker_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackageRegistryCleanupPoliciesWorkerCapacity", []))

    @jsii.member(jsii_name="resetPagesDomainVerificationEnabled")
    def reset_pages_domain_verification_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPagesDomainVerificationEnabled", []))

    @jsii.member(jsii_name="resetPasswordAuthenticationEnabledForGit")
    def reset_password_authentication_enabled_for_git(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordAuthenticationEnabledForGit", []))

    @jsii.member(jsii_name="resetPasswordAuthenticationEnabledForWeb")
    def reset_password_authentication_enabled_for_web(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordAuthenticationEnabledForWeb", []))

    @jsii.member(jsii_name="resetPasswordLowercaseRequired")
    def reset_password_lowercase_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordLowercaseRequired", []))

    @jsii.member(jsii_name="resetPasswordNumberRequired")
    def reset_password_number_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordNumberRequired", []))

    @jsii.member(jsii_name="resetPasswordSymbolRequired")
    def reset_password_symbol_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordSymbolRequired", []))

    @jsii.member(jsii_name="resetPasswordUppercaseRequired")
    def reset_password_uppercase_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordUppercaseRequired", []))

    @jsii.member(jsii_name="resetPerformanceBarAllowedGroupPath")
    def reset_performance_bar_allowed_group_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerformanceBarAllowedGroupPath", []))

    @jsii.member(jsii_name="resetPersonalAccessTokenPrefix")
    def reset_personal_access_token_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPersonalAccessTokenPrefix", []))

    @jsii.member(jsii_name="resetPipelineLimitPerProjectUserSha")
    def reset_pipeline_limit_per_project_user_sha(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipelineLimitPerProjectUserSha", []))

    @jsii.member(jsii_name="resetPlantumlEnabled")
    def reset_plantuml_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlantumlEnabled", []))

    @jsii.member(jsii_name="resetPlantumlUrl")
    def reset_plantuml_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlantumlUrl", []))

    @jsii.member(jsii_name="resetPollingIntervalMultiplier")
    def reset_polling_interval_multiplier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPollingIntervalMultiplier", []))

    @jsii.member(jsii_name="resetProjectExportEnabled")
    def reset_project_export_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectExportEnabled", []))

    @jsii.member(jsii_name="resetPrometheusMetricsEnabled")
    def reset_prometheus_metrics_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrometheusMetricsEnabled", []))

    @jsii.member(jsii_name="resetProtectedCiVariables")
    def reset_protected_ci_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtectedCiVariables", []))

    @jsii.member(jsii_name="resetPushEventActivitiesLimit")
    def reset_push_event_activities_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushEventActivitiesLimit", []))

    @jsii.member(jsii_name="resetPushEventHooksLimit")
    def reset_push_event_hooks_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushEventHooksLimit", []))

    @jsii.member(jsii_name="resetPypiPackageRequestsForwarding")
    def reset_pypi_package_requests_forwarding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPypiPackageRequestsForwarding", []))

    @jsii.member(jsii_name="resetRateLimitingResponseText")
    def reset_rate_limiting_response_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimitingResponseText", []))

    @jsii.member(jsii_name="resetRawBlobRequestLimit")
    def reset_raw_blob_request_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRawBlobRequestLimit", []))

    @jsii.member(jsii_name="resetRecaptchaEnabled")
    def reset_recaptcha_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecaptchaEnabled", []))

    @jsii.member(jsii_name="resetRecaptchaPrivateKey")
    def reset_recaptcha_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecaptchaPrivateKey", []))

    @jsii.member(jsii_name="resetRecaptchaSiteKey")
    def reset_recaptcha_site_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecaptchaSiteKey", []))

    @jsii.member(jsii_name="resetReceiveMaxInputSize")
    def reset_receive_max_input_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReceiveMaxInputSize", []))

    @jsii.member(jsii_name="resetRepositoryChecksEnabled")
    def reset_repository_checks_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryChecksEnabled", []))

    @jsii.member(jsii_name="resetRepositorySizeLimit")
    def reset_repository_size_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositorySizeLimit", []))

    @jsii.member(jsii_name="resetRepositoryStorages")
    def reset_repository_storages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryStorages", []))

    @jsii.member(jsii_name="resetRepositoryStoragesWeighted")
    def reset_repository_storages_weighted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryStoragesWeighted", []))

    @jsii.member(jsii_name="resetRequireAdminApprovalAfterUserSignup")
    def reset_require_admin_approval_after_user_signup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireAdminApprovalAfterUserSignup", []))

    @jsii.member(jsii_name="resetRequireTwoFactorAuthentication")
    def reset_require_two_factor_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireTwoFactorAuthentication", []))

    @jsii.member(jsii_name="resetRestrictedVisibilityLevels")
    def reset_restricted_visibility_levels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestrictedVisibilityLevels", []))

    @jsii.member(jsii_name="resetRsaKeyRestriction")
    def reset_rsa_key_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRsaKeyRestriction", []))

    @jsii.member(jsii_name="resetSearchRateLimit")
    def reset_search_rate_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchRateLimit", []))

    @jsii.member(jsii_name="resetSearchRateLimitUnauthenticated")
    def reset_search_rate_limit_unauthenticated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchRateLimitUnauthenticated", []))

    @jsii.member(jsii_name="resetSendUserConfirmationEmail")
    def reset_send_user_confirmation_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendUserConfirmationEmail", []))

    @jsii.member(jsii_name="resetSessionExpireDelay")
    def reset_session_expire_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionExpireDelay", []))

    @jsii.member(jsii_name="resetSharedRunnersEnabled")
    def reset_shared_runners_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedRunnersEnabled", []))

    @jsii.member(jsii_name="resetSharedRunnersMinutes")
    def reset_shared_runners_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedRunnersMinutes", []))

    @jsii.member(jsii_name="resetSharedRunnersText")
    def reset_shared_runners_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedRunnersText", []))

    @jsii.member(jsii_name="resetSidekiqJobLimiterCompressionThresholdBytes")
    def reset_sidekiq_job_limiter_compression_threshold_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSidekiqJobLimiterCompressionThresholdBytes", []))

    @jsii.member(jsii_name="resetSidekiqJobLimiterLimitBytes")
    def reset_sidekiq_job_limiter_limit_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSidekiqJobLimiterLimitBytes", []))

    @jsii.member(jsii_name="resetSidekiqJobLimiterMode")
    def reset_sidekiq_job_limiter_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSidekiqJobLimiterMode", []))

    @jsii.member(jsii_name="resetSignInText")
    def reset_sign_in_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignInText", []))

    @jsii.member(jsii_name="resetSignupEnabled")
    def reset_signup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignupEnabled", []))

    @jsii.member(jsii_name="resetSlackAppEnabled")
    def reset_slack_app_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlackAppEnabled", []))

    @jsii.member(jsii_name="resetSlackAppId")
    def reset_slack_app_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlackAppId", []))

    @jsii.member(jsii_name="resetSlackAppSecret")
    def reset_slack_app_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlackAppSecret", []))

    @jsii.member(jsii_name="resetSlackAppSigningSecret")
    def reset_slack_app_signing_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlackAppSigningSecret", []))

    @jsii.member(jsii_name="resetSlackAppVerificationToken")
    def reset_slack_app_verification_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlackAppVerificationToken", []))

    @jsii.member(jsii_name="resetSnippetSizeLimit")
    def reset_snippet_size_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnippetSizeLimit", []))

    @jsii.member(jsii_name="resetSnowplowAppId")
    def reset_snowplow_app_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowplowAppId", []))

    @jsii.member(jsii_name="resetSnowplowCollectorHostname")
    def reset_snowplow_collector_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowplowCollectorHostname", []))

    @jsii.member(jsii_name="resetSnowplowCookieDomain")
    def reset_snowplow_cookie_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowplowCookieDomain", []))

    @jsii.member(jsii_name="resetSnowplowEnabled")
    def reset_snowplow_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowplowEnabled", []))

    @jsii.member(jsii_name="resetSourcegraphEnabled")
    def reset_sourcegraph_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourcegraphEnabled", []))

    @jsii.member(jsii_name="resetSourcegraphPublicOnly")
    def reset_sourcegraph_public_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourcegraphPublicOnly", []))

    @jsii.member(jsii_name="resetSourcegraphUrl")
    def reset_sourcegraph_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourcegraphUrl", []))

    @jsii.member(jsii_name="resetSpamCheckApiKey")
    def reset_spam_check_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpamCheckApiKey", []))

    @jsii.member(jsii_name="resetSpamCheckEndpointEnabled")
    def reset_spam_check_endpoint_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpamCheckEndpointEnabled", []))

    @jsii.member(jsii_name="resetSpamCheckEndpointUrl")
    def reset_spam_check_endpoint_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpamCheckEndpointUrl", []))

    @jsii.member(jsii_name="resetSuggestPipelineEnabled")
    def reset_suggest_pipeline_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuggestPipelineEnabled", []))

    @jsii.member(jsii_name="resetTerminalMaxSessionTime")
    def reset_terminal_max_session_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminalMaxSessionTime", []))

    @jsii.member(jsii_name="resetTerms")
    def reset_terms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerms", []))

    @jsii.member(jsii_name="resetThrottleAuthenticatedApiEnabled")
    def reset_throttle_authenticated_api_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleAuthenticatedApiEnabled", []))

    @jsii.member(jsii_name="resetThrottleAuthenticatedApiPeriodInSeconds")
    def reset_throttle_authenticated_api_period_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleAuthenticatedApiPeriodInSeconds", []))

    @jsii.member(jsii_name="resetThrottleAuthenticatedApiRequestsPerPeriod")
    def reset_throttle_authenticated_api_requests_per_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleAuthenticatedApiRequestsPerPeriod", []))

    @jsii.member(jsii_name="resetThrottleAuthenticatedPackagesApiEnabled")
    def reset_throttle_authenticated_packages_api_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleAuthenticatedPackagesApiEnabled", []))

    @jsii.member(jsii_name="resetThrottleAuthenticatedPackagesApiPeriodInSeconds")
    def reset_throttle_authenticated_packages_api_period_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleAuthenticatedPackagesApiPeriodInSeconds", []))

    @jsii.member(jsii_name="resetThrottleAuthenticatedPackagesApiRequestsPerPeriod")
    def reset_throttle_authenticated_packages_api_requests_per_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleAuthenticatedPackagesApiRequestsPerPeriod", []))

    @jsii.member(jsii_name="resetThrottleAuthenticatedWebEnabled")
    def reset_throttle_authenticated_web_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleAuthenticatedWebEnabled", []))

    @jsii.member(jsii_name="resetThrottleAuthenticatedWebPeriodInSeconds")
    def reset_throttle_authenticated_web_period_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleAuthenticatedWebPeriodInSeconds", []))

    @jsii.member(jsii_name="resetThrottleAuthenticatedWebRequestsPerPeriod")
    def reset_throttle_authenticated_web_requests_per_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleAuthenticatedWebRequestsPerPeriod", []))

    @jsii.member(jsii_name="resetThrottleUnauthenticatedApiEnabled")
    def reset_throttle_unauthenticated_api_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleUnauthenticatedApiEnabled", []))

    @jsii.member(jsii_name="resetThrottleUnauthenticatedApiPeriodInSeconds")
    def reset_throttle_unauthenticated_api_period_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleUnauthenticatedApiPeriodInSeconds", []))

    @jsii.member(jsii_name="resetThrottleUnauthenticatedApiRequestsPerPeriod")
    def reset_throttle_unauthenticated_api_requests_per_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleUnauthenticatedApiRequestsPerPeriod", []))

    @jsii.member(jsii_name="resetThrottleUnauthenticatedPackagesApiEnabled")
    def reset_throttle_unauthenticated_packages_api_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleUnauthenticatedPackagesApiEnabled", []))

    @jsii.member(jsii_name="resetThrottleUnauthenticatedPackagesApiPeriodInSeconds")
    def reset_throttle_unauthenticated_packages_api_period_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleUnauthenticatedPackagesApiPeriodInSeconds", []))

    @jsii.member(jsii_name="resetThrottleUnauthenticatedPackagesApiRequestsPerPeriod")
    def reset_throttle_unauthenticated_packages_api_requests_per_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleUnauthenticatedPackagesApiRequestsPerPeriod", []))

    @jsii.member(jsii_name="resetThrottleUnauthenticatedWebEnabled")
    def reset_throttle_unauthenticated_web_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleUnauthenticatedWebEnabled", []))

    @jsii.member(jsii_name="resetThrottleUnauthenticatedWebPeriodInSeconds")
    def reset_throttle_unauthenticated_web_period_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleUnauthenticatedWebPeriodInSeconds", []))

    @jsii.member(jsii_name="resetThrottleUnauthenticatedWebRequestsPerPeriod")
    def reset_throttle_unauthenticated_web_requests_per_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottleUnauthenticatedWebRequestsPerPeriod", []))

    @jsii.member(jsii_name="resetTimeTrackingLimitToHours")
    def reset_time_tracking_limit_to_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeTrackingLimitToHours", []))

    @jsii.member(jsii_name="resetTwoFactorGracePeriod")
    def reset_two_factor_grace_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTwoFactorGracePeriod", []))

    @jsii.member(jsii_name="resetUniqueIpsLimitEnabled")
    def reset_unique_ips_limit_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniqueIpsLimitEnabled", []))

    @jsii.member(jsii_name="resetUniqueIpsLimitPerUser")
    def reset_unique_ips_limit_per_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniqueIpsLimitPerUser", []))

    @jsii.member(jsii_name="resetUniqueIpsLimitTimeWindow")
    def reset_unique_ips_limit_time_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniqueIpsLimitTimeWindow", []))

    @jsii.member(jsii_name="resetUsagePingEnabled")
    def reset_usage_ping_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsagePingEnabled", []))

    @jsii.member(jsii_name="resetUserDeactivationEmailsEnabled")
    def reset_user_deactivation_emails_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDeactivationEmailsEnabled", []))

    @jsii.member(jsii_name="resetUserDefaultExternal")
    def reset_user_default_external(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDefaultExternal", []))

    @jsii.member(jsii_name="resetUserDefaultInternalRegex")
    def reset_user_default_internal_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDefaultInternalRegex", []))

    @jsii.member(jsii_name="resetUserOauthApplications")
    def reset_user_oauth_applications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserOauthApplications", []))

    @jsii.member(jsii_name="resetUserShowAddSshKeyMessage")
    def reset_user_show_add_ssh_key_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserShowAddSshKeyMessage", []))

    @jsii.member(jsii_name="resetVersionCheckEnabled")
    def reset_version_check_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionCheckEnabled", []))

    @jsii.member(jsii_name="resetWebIdeClientsidePreviewEnabled")
    def reset_web_ide_clientside_preview_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebIdeClientsidePreviewEnabled", []))

    @jsii.member(jsii_name="resetWhatsNewVariant")
    def reset_whats_new_variant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhatsNewVariant", []))

    @jsii.member(jsii_name="resetWikiPageMaxContentBytes")
    def reset_wiki_page_max_content_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWikiPageMaxContentBytes", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="abuseNotificationEmailInput")
    def abuse_notification_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "abuseNotificationEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="adminModeInput")
    def admin_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adminModeInput"))

    @builtins.property
    @jsii.member(jsii_name="afterSignOutPathInput")
    def after_sign_out_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "afterSignOutPathInput"))

    @builtins.property
    @jsii.member(jsii_name="afterSignUpTextInput")
    def after_sign_up_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "afterSignUpTextInput"))

    @builtins.property
    @jsii.member(jsii_name="akismetApiKeyInput")
    def akismet_api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "akismetApiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="akismetEnabledInput")
    def akismet_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "akismetEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="allowGroupOwnersToManageLdapInput")
    def allow_group_owners_to_manage_ldap_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowGroupOwnersToManageLdapInput"))

    @builtins.property
    @jsii.member(jsii_name="allowLocalRequestsFromSystemHooksInput")
    def allow_local_requests_from_system_hooks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowLocalRequestsFromSystemHooksInput"))

    @builtins.property
    @jsii.member(jsii_name="allowLocalRequestsFromWebHooksAndServicesInput")
    def allow_local_requests_from_web_hooks_and_services_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowLocalRequestsFromWebHooksAndServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveBuildsInHumanReadableInput")
    def archive_builds_in_human_readable_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "archiveBuildsInHumanReadableInput"))

    @builtins.property
    @jsii.member(jsii_name="assetProxyAllowlistInput")
    def asset_proxy_allowlist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "assetProxyAllowlistInput"))

    @builtins.property
    @jsii.member(jsii_name="assetProxyEnabledInput")
    def asset_proxy_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "assetProxyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="assetProxySecretKeyInput")
    def asset_proxy_secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetProxySecretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="assetProxyUrlInput")
    def asset_proxy_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assetProxyUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedKeysEnabledInput")
    def authorized_keys_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "authorizedKeysEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDevopsDomainInput")
    def auto_devops_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoDevopsDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="autoDevopsEnabledInput")
    def auto_devops_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoDevopsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticPurchasedStorageAllocationInput")
    def automatic_purchased_storage_allocation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automaticPurchasedStorageAllocationInput"))

    @builtins.property
    @jsii.member(jsii_name="canCreateGroupInput")
    def can_create_group_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "canCreateGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="checkNamespacePlanInput")
    def check_namespace_plan_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "checkNamespacePlanInput"))

    @builtins.property
    @jsii.member(jsii_name="commitEmailHostnameInput")
    def commit_email_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commitEmailHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerExpirationPoliciesEnableHistoricEntriesInput")
    def container_expiration_policies_enable_historic_entries_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "containerExpirationPoliciesEnableHistoricEntriesInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryCleanupTagsServiceMaxListSizeInput")
    def container_registry_cleanup_tags_service_max_list_size_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerRegistryCleanupTagsServiceMaxListSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryDeleteTagsServiceTimeoutInput")
    def container_registry_delete_tags_service_timeout_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerRegistryDeleteTagsServiceTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryExpirationPoliciesCachingInput")
    def container_registry_expiration_policies_caching_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "containerRegistryExpirationPoliciesCachingInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryExpirationPoliciesWorkerCapacityInput")
    def container_registry_expiration_policies_worker_capacity_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerRegistryExpirationPoliciesWorkerCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryTokenExpireDelayInput")
    def container_registry_token_expire_delay_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerRegistryTokenExpireDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="deactivateDormantUsersInput")
    def deactivate_dormant_users_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deactivateDormantUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultArtifactsExpireInInput")
    def default_artifacts_expire_in_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultArtifactsExpireInInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranchNameInput")
    def default_branch_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBranchNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranchProtectionInput")
    def default_branch_protection_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultBranchProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultCiConfigPathInput")
    def default_ci_config_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultCiConfigPathInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultGroupVisibilityInput")
    def default_group_visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultGroupVisibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultProjectCreationInput")
    def default_project_creation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultProjectCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultProjectsLimitInput")
    def default_projects_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultProjectsLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultProjectVisibilityInput")
    def default_project_visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultProjectVisibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSnippetVisibilityInput")
    def default_snippet_visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSnippetVisibilityInput"))

    @builtins.property
    @jsii.member(jsii_name="delayedGroupDeletionInput")
    def delayed_group_deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "delayedGroupDeletionInput"))

    @builtins.property
    @jsii.member(jsii_name="delayedProjectDeletionInput")
    def delayed_project_deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "delayedProjectDeletionInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInactiveProjectsInput")
    def delete_inactive_projects_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteInactiveProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionAdjournedPeriodInput")
    def deletion_adjourned_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deletionAdjournedPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="diffMaxFilesInput")
    def diff_max_files_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diffMaxFilesInput"))

    @builtins.property
    @jsii.member(jsii_name="diffMaxLinesInput")
    def diff_max_lines_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diffMaxLinesInput"))

    @builtins.property
    @jsii.member(jsii_name="diffMaxPatchBytesInput")
    def diff_max_patch_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diffMaxPatchBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledOauthSignInSourcesInput")
    def disabled_oauth_sign_in_sources_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "disabledOauthSignInSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="disableFeedTokenInput")
    def disable_feed_token_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableFeedTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsRebindingProtectionEnabledInput")
    def dns_rebinding_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dnsRebindingProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="domainAllowlistInput")
    def domain_allowlist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainAllowlistInput"))

    @builtins.property
    @jsii.member(jsii_name="domainDenylistEnabledInput")
    def domain_denylist_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "domainDenylistEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="domainDenylistInput")
    def domain_denylist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainDenylistInput"))

    @builtins.property
    @jsii.member(jsii_name="dsaKeyRestrictionInput")
    def dsa_key_restriction_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dsaKeyRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="ecdsaKeyRestrictionInput")
    def ecdsa_key_restriction_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ecdsaKeyRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="ecdsaSkKeyRestrictionInput")
    def ecdsa_sk_key_restriction_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ecdsaSkKeyRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="ed25519KeyRestrictionInput")
    def ed25519_key_restriction_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ed25519KeyRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="ed25519SkKeyRestrictionInput")
    def ed25519_sk_key_restriction_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ed25519SkKeyRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="eksAccessKeyIdInput")
    def eks_access_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eksAccessKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="eksAccountIdInput")
    def eks_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eksAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="eksIntegrationEnabledInput")
    def eks_integration_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "eksIntegrationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eksSecretAccessKeyInput")
    def eks_secret_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eksSecretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchAwsAccessKeyInput")
    def elasticsearch_aws_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchAwsAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchAwsInput")
    def elasticsearch_aws_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "elasticsearchAwsInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchAwsRegionInput")
    def elasticsearch_aws_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchAwsRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchAwsSecretAccessKeyInput")
    def elasticsearch_aws_secret_access_key_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchAwsSecretAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchIndexedFieldLengthLimitInput")
    def elasticsearch_indexed_field_length_limit_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "elasticsearchIndexedFieldLengthLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchIndexedFileSizeLimitKbInput")
    def elasticsearch_indexed_file_size_limit_kb_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "elasticsearchIndexedFileSizeLimitKbInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchIndexingInput")
    def elasticsearch_indexing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "elasticsearchIndexingInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchLimitIndexingInput")
    def elasticsearch_limit_indexing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "elasticsearchLimitIndexingInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchMaxBulkConcurrencyInput")
    def elasticsearch_max_bulk_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "elasticsearchMaxBulkConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchMaxBulkSizeMbInput")
    def elasticsearch_max_bulk_size_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "elasticsearchMaxBulkSizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchNamespaceIdsInput")
    def elasticsearch_namespace_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "elasticsearchNamespaceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchPasswordInput")
    def elasticsearch_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchProjectIdsInput")
    def elasticsearch_project_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "elasticsearchProjectIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchSearchInput")
    def elasticsearch_search_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "elasticsearchSearchInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchUrlInput")
    def elasticsearch_url_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "elasticsearchUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchUsernameInput")
    def elasticsearch_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAdditionalTextInput")
    def email_additional_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailAdditionalTextInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAuthorInBodyInput")
    def email_author_in_body_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "emailAuthorInBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledGitAccessProtocolInput")
    def enabled_git_access_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enabledGitAccessProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceNamespaceStorageLimitInput")
    def enforce_namespace_storage_limit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceNamespaceStorageLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceTermsInput")
    def enforce_terms_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceTermsInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAuthClientCertInput")
    def external_auth_client_cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalAuthClientCertInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAuthClientKeyInput")
    def external_auth_client_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalAuthClientKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAuthClientKeyPassInput")
    def external_auth_client_key_pass_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalAuthClientKeyPassInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAuthorizationServiceDefaultLabelInput")
    def external_authorization_service_default_label_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalAuthorizationServiceDefaultLabelInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAuthorizationServiceEnabledInput")
    def external_authorization_service_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "externalAuthorizationServiceEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAuthorizationServiceTimeoutInput")
    def external_authorization_service_timeout_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "externalAuthorizationServiceTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAuthorizationServiceUrlInput")
    def external_authorization_service_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalAuthorizationServiceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="externalPipelineValidationServiceTimeoutInput")
    def external_pipeline_validation_service_timeout_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "externalPipelineValidationServiceTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="externalPipelineValidationServiceTokenInput")
    def external_pipeline_validation_service_token_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalPipelineValidationServiceTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="externalPipelineValidationServiceUrlInput")
    def external_pipeline_validation_service_url_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalPipelineValidationServiceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="fileTemplateProjectIdInput")
    def file_template_project_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fileTemplateProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="firstDayOfWeekInput")
    def first_day_of_week_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "firstDayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="geoNodeAllowedIpsInput")
    def geo_node_allowed_ips_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "geoNodeAllowedIpsInput"))

    @builtins.property
    @jsii.member(jsii_name="geoStatusTimeoutInput")
    def geo_status_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "geoStatusTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="gitalyTimeoutDefaultInput")
    def gitaly_timeout_default_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gitalyTimeoutDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="gitalyTimeoutFastInput")
    def gitaly_timeout_fast_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gitalyTimeoutFastInput"))

    @builtins.property
    @jsii.member(jsii_name="gitalyTimeoutMediumInput")
    def gitaly_timeout_medium_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gitalyTimeoutMediumInput"))

    @builtins.property
    @jsii.member(jsii_name="gitRateLimitUsersAllowlistInput")
    def git_rate_limit_users_allowlist_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "gitRateLimitUsersAllowlistInput"))

    @builtins.property
    @jsii.member(jsii_name="gitTwoFactorSessionExpiryInput")
    def git_two_factor_session_expiry_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gitTwoFactorSessionExpiryInput"))

    @builtins.property
    @jsii.member(jsii_name="grafanaEnabledInput")
    def grafana_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "grafanaEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="grafanaUrlInput")
    def grafana_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grafanaUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="gravatarEnabledInput")
    def gravatar_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "gravatarEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="groupOwnersCanManageDefaultBranchProtectionInput")
    def group_owners_can_manage_default_branch_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "groupOwnersCanManageDefaultBranchProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="hashedStorageEnabledInput")
    def hashed_storage_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hashedStorageEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="helpPageHideCommercialContentInput")
    def help_page_hide_commercial_content_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "helpPageHideCommercialContentInput"))

    @builtins.property
    @jsii.member(jsii_name="helpPageSupportUrlInput")
    def help_page_support_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "helpPageSupportUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="helpPageTextInput")
    def help_page_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "helpPageTextInput"))

    @builtins.property
    @jsii.member(jsii_name="helpTextInput")
    def help_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "helpTextInput"))

    @builtins.property
    @jsii.member(jsii_name="hideThirdPartyOffersInput")
    def hide_third_party_offers_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hideThirdPartyOffersInput"))

    @builtins.property
    @jsii.member(jsii_name="homePageUrlInput")
    def home_page_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homePageUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="housekeepingEnabledInput")
    def housekeeping_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "housekeepingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="housekeepingFullRepackPeriodInput")
    def housekeeping_full_repack_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "housekeepingFullRepackPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="housekeepingGcPeriodInput")
    def housekeeping_gc_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "housekeepingGcPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="housekeepingIncrementalRepackPeriodInput")
    def housekeeping_incremental_repack_period_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "housekeepingIncrementalRepackPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="htmlEmailsEnabledInput")
    def html_emails_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "htmlEmailsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importSourcesInput")
    def import_sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "importSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="inactiveProjectsDeleteAfterMonthsInput")
    def inactive_projects_delete_after_months_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "inactiveProjectsDeleteAfterMonthsInput"))

    @builtins.property
    @jsii.member(jsii_name="inactiveProjectsMinSizeMbInput")
    def inactive_projects_min_size_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "inactiveProjectsMinSizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="inactiveProjectsSendWarningEmailAfterMonthsInput")
    def inactive_projects_send_warning_email_after_months_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "inactiveProjectsSendWarningEmailAfterMonthsInput"))

    @builtins.property
    @jsii.member(jsii_name="inProductMarketingEmailsEnabledInput")
    def in_product_marketing_emails_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inProductMarketingEmailsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="invisibleCaptchaEnabledInput")
    def invisible_captcha_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invisibleCaptchaEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="issuesCreateLimitInput")
    def issues_create_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "issuesCreateLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="keepLatestArtifactInput")
    def keep_latest_artifact_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepLatestArtifactInput"))

    @builtins.property
    @jsii.member(jsii_name="localMarkdownVersionInput")
    def local_markdown_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "localMarkdownVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="mailgunEventsEnabledInput")
    def mailgun_events_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mailgunEventsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="mailgunSigningKeyInput")
    def mailgun_signing_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mailgunSigningKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceModeInput")
    def maintenance_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "maintenanceModeInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceModeMessageInput")
    def maintenance_mode_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceModeMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="maxArtifactsSizeInput")
    def max_artifacts_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxArtifactsSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAttachmentSizeInput")
    def max_attachment_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAttachmentSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxExportSizeInput")
    def max_export_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxExportSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxImportSizeInput")
    def max_import_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxImportSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNumberOfRepositoryDownloadsInput")
    def max_number_of_repository_downloads_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNumberOfRepositoryDownloadsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNumberOfRepositoryDownloadsWithinTimePeriodInput")
    def max_number_of_repository_downloads_within_time_period_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNumberOfRepositoryDownloadsWithinTimePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPagesSizeInput")
    def max_pages_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPagesSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPersonalAccessTokenLifetimeInput")
    def max_personal_access_token_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPersonalAccessTokenLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSshKeyLifetimeInput")
    def max_ssh_key_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSshKeyLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsMethodCallThresholdInput")
    def metrics_method_call_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsMethodCallThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="mirrorAvailableInput")
    def mirror_available_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mirrorAvailableInput"))

    @builtins.property
    @jsii.member(jsii_name="mirrorCapacityThresholdInput")
    def mirror_capacity_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mirrorCapacityThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="mirrorMaxCapacityInput")
    def mirror_max_capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mirrorMaxCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="mirrorMaxDelayInput")
    def mirror_max_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mirrorMaxDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="npmPackageRequestsForwardingInput")
    def npm_package_requests_forwarding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "npmPackageRequestsForwardingInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundLocalRequestsWhitelistInput")
    def outbound_local_requests_whitelist_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outboundLocalRequestsWhitelistInput"))

    @builtins.property
    @jsii.member(jsii_name="packageRegistryCleanupPoliciesWorkerCapacityInput")
    def package_registry_cleanup_policies_worker_capacity_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "packageRegistryCleanupPoliciesWorkerCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="pagesDomainVerificationEnabledInput")
    def pages_domain_verification_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pagesDomainVerificationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordAuthenticationEnabledForGitInput")
    def password_authentication_enabled_for_git_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordAuthenticationEnabledForGitInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordAuthenticationEnabledForWebInput")
    def password_authentication_enabled_for_web_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordAuthenticationEnabledForWebInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordLowercaseRequiredInput")
    def password_lowercase_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordLowercaseRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordNumberRequiredInput")
    def password_number_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordNumberRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordSymbolRequiredInput")
    def password_symbol_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordSymbolRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordUppercaseRequiredInput")
    def password_uppercase_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordUppercaseRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="performanceBarAllowedGroupPathInput")
    def performance_bar_allowed_group_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "performanceBarAllowedGroupPathInput"))

    @builtins.property
    @jsii.member(jsii_name="personalAccessTokenPrefixInput")
    def personal_access_token_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "personalAccessTokenPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="pipelineLimitPerProjectUserShaInput")
    def pipeline_limit_per_project_user_sha_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pipelineLimitPerProjectUserShaInput"))

    @builtins.property
    @jsii.member(jsii_name="plantumlEnabledInput")
    def plantuml_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "plantumlEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="plantumlUrlInput")
    def plantuml_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "plantumlUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="pollingIntervalMultiplierInput")
    def polling_interval_multiplier_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pollingIntervalMultiplierInput"))

    @builtins.property
    @jsii.member(jsii_name="projectExportEnabledInput")
    def project_export_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "projectExportEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="prometheusMetricsEnabledInput")
    def prometheus_metrics_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "prometheusMetricsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="protectedCiVariablesInput")
    def protected_ci_variables_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "protectedCiVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="pushEventActivitiesLimitInput")
    def push_event_activities_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pushEventActivitiesLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="pushEventHooksLimitInput")
    def push_event_hooks_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pushEventHooksLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="pypiPackageRequestsForwardingInput")
    def pypi_package_requests_forwarding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pypiPackageRequestsForwardingInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitingResponseTextInput")
    def rate_limiting_response_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rateLimitingResponseTextInput"))

    @builtins.property
    @jsii.member(jsii_name="rawBlobRequestLimitInput")
    def raw_blob_request_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rawBlobRequestLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="recaptchaEnabledInput")
    def recaptcha_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "recaptchaEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="recaptchaPrivateKeyInput")
    def recaptcha_private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recaptchaPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="recaptchaSiteKeyInput")
    def recaptcha_site_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recaptchaSiteKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="receiveMaxInputSizeInput")
    def receive_max_input_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "receiveMaxInputSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryChecksEnabledInput")
    def repository_checks_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "repositoryChecksEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="repositorySizeLimitInput")
    def repository_size_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "repositorySizeLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryStoragesInput")
    def repository_storages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "repositoryStoragesInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryStoragesWeightedInput")
    def repository_storages_weighted_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], jsii.get(self, "repositoryStoragesWeightedInput"))

    @builtins.property
    @jsii.member(jsii_name="requireAdminApprovalAfterUserSignupInput")
    def require_admin_approval_after_user_signup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireAdminApprovalAfterUserSignupInput"))

    @builtins.property
    @jsii.member(jsii_name="requireTwoFactorAuthenticationInput")
    def require_two_factor_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireTwoFactorAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="restrictedVisibilityLevelsInput")
    def restricted_visibility_levels_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedVisibilityLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="rsaKeyRestrictionInput")
    def rsa_key_restriction_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rsaKeyRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="searchRateLimitInput")
    def search_rate_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "searchRateLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="searchRateLimitUnauthenticatedInput")
    def search_rate_limit_unauthenticated_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "searchRateLimitUnauthenticatedInput"))

    @builtins.property
    @jsii.member(jsii_name="sendUserConfirmationEmailInput")
    def send_user_confirmation_email_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendUserConfirmationEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionExpireDelayInput")
    def session_expire_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionExpireDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersEnabledInput")
    def shared_runners_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sharedRunnersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersMinutesInput")
    def shared_runners_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sharedRunnersMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersTextInput")
    def shared_runners_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedRunnersTextInput"))

    @builtins.property
    @jsii.member(jsii_name="sidekiqJobLimiterCompressionThresholdBytesInput")
    def sidekiq_job_limiter_compression_threshold_bytes_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sidekiqJobLimiterCompressionThresholdBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="sidekiqJobLimiterLimitBytesInput")
    def sidekiq_job_limiter_limit_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sidekiqJobLimiterLimitBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="sidekiqJobLimiterModeInput")
    def sidekiq_job_limiter_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sidekiqJobLimiterModeInput"))

    @builtins.property
    @jsii.member(jsii_name="signInTextInput")
    def sign_in_text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signInTextInput"))

    @builtins.property
    @jsii.member(jsii_name="signupEnabledInput")
    def signup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "signupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="slackAppEnabledInput")
    def slack_app_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "slackAppEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="slackAppIdInput")
    def slack_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slackAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="slackAppSecretInput")
    def slack_app_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slackAppSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="slackAppSigningSecretInput")
    def slack_app_signing_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slackAppSigningSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="slackAppVerificationTokenInput")
    def slack_app_verification_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "slackAppVerificationTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="snippetSizeLimitInput")
    def snippet_size_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snippetSizeLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="snowplowAppIdInput")
    def snowplow_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snowplowAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="snowplowCollectorHostnameInput")
    def snowplow_collector_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snowplowCollectorHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="snowplowCookieDomainInput")
    def snowplow_cookie_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snowplowCookieDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="snowplowEnabledInput")
    def snowplow_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "snowplowEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcegraphEnabledInput")
    def sourcegraph_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sourcegraphEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcegraphPublicOnlyInput")
    def sourcegraph_public_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sourcegraphPublicOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcegraphUrlInput")
    def sourcegraph_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourcegraphUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="spamCheckApiKeyInput")
    def spam_check_api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spamCheckApiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="spamCheckEndpointEnabledInput")
    def spam_check_endpoint_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "spamCheckEndpointEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="spamCheckEndpointUrlInput")
    def spam_check_endpoint_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spamCheckEndpointUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="suggestPipelineEnabledInput")
    def suggest_pipeline_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suggestPipelineEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="terminalMaxSessionTimeInput")
    def terminal_max_session_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "terminalMaxSessionTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="termsInput")
    def terms_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "termsInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedApiEnabledInput")
    def throttle_authenticated_api_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "throttleAuthenticatedApiEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedApiPeriodInSecondsInput")
    def throttle_authenticated_api_period_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleAuthenticatedApiPeriodInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedApiRequestsPerPeriodInput")
    def throttle_authenticated_api_requests_per_period_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleAuthenticatedApiRequestsPerPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedPackagesApiEnabledInput")
    def throttle_authenticated_packages_api_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "throttleAuthenticatedPackagesApiEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedPackagesApiPeriodInSecondsInput")
    def throttle_authenticated_packages_api_period_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleAuthenticatedPackagesApiPeriodInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedPackagesApiRequestsPerPeriodInput")
    def throttle_authenticated_packages_api_requests_per_period_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleAuthenticatedPackagesApiRequestsPerPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedWebEnabledInput")
    def throttle_authenticated_web_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "throttleAuthenticatedWebEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedWebPeriodInSecondsInput")
    def throttle_authenticated_web_period_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleAuthenticatedWebPeriodInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedWebRequestsPerPeriodInput")
    def throttle_authenticated_web_requests_per_period_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleAuthenticatedWebRequestsPerPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedApiEnabledInput")
    def throttle_unauthenticated_api_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "throttleUnauthenticatedApiEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedApiPeriodInSecondsInput")
    def throttle_unauthenticated_api_period_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleUnauthenticatedApiPeriodInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedApiRequestsPerPeriodInput")
    def throttle_unauthenticated_api_requests_per_period_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleUnauthenticatedApiRequestsPerPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedPackagesApiEnabledInput")
    def throttle_unauthenticated_packages_api_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "throttleUnauthenticatedPackagesApiEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedPackagesApiPeriodInSecondsInput")
    def throttle_unauthenticated_packages_api_period_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleUnauthenticatedPackagesApiPeriodInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedPackagesApiRequestsPerPeriodInput")
    def throttle_unauthenticated_packages_api_requests_per_period_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleUnauthenticatedPackagesApiRequestsPerPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedWebEnabledInput")
    def throttle_unauthenticated_web_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "throttleUnauthenticatedWebEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedWebPeriodInSecondsInput")
    def throttle_unauthenticated_web_period_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleUnauthenticatedWebPeriodInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedWebRequestsPerPeriodInput")
    def throttle_unauthenticated_web_requests_per_period_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttleUnauthenticatedWebRequestsPerPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="timeTrackingLimitToHoursInput")
    def time_tracking_limit_to_hours_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeTrackingLimitToHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="twoFactorGracePeriodInput")
    def two_factor_grace_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "twoFactorGracePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueIpsLimitEnabledInput")
    def unique_ips_limit_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "uniqueIpsLimitEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueIpsLimitPerUserInput")
    def unique_ips_limit_per_user_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "uniqueIpsLimitPerUserInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueIpsLimitTimeWindowInput")
    def unique_ips_limit_time_window_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "uniqueIpsLimitTimeWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="usagePingEnabledInput")
    def usage_ping_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "usagePingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="userDeactivationEmailsEnabledInput")
    def user_deactivation_emails_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "userDeactivationEmailsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="userDefaultExternalInput")
    def user_default_external_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "userDefaultExternalInput"))

    @builtins.property
    @jsii.member(jsii_name="userDefaultInternalRegexInput")
    def user_default_internal_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDefaultInternalRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="userOauthApplicationsInput")
    def user_oauth_applications_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "userOauthApplicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="userShowAddSshKeyMessageInput")
    def user_show_add_ssh_key_message_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "userShowAddSshKeyMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="versionCheckEnabledInput")
    def version_check_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "versionCheckEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="webIdeClientsidePreviewEnabledInput")
    def web_ide_clientside_preview_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "webIdeClientsidePreviewEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="whatsNewVariantInput")
    def whats_new_variant_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "whatsNewVariantInput"))

    @builtins.property
    @jsii.member(jsii_name="wikiPageMaxContentBytesInput")
    def wiki_page_max_content_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "wikiPageMaxContentBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="abuseNotificationEmail")
    def abuse_notification_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "abuseNotificationEmail"))

    @abuse_notification_email.setter
    def abuse_notification_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa573503a4f45938a3f93c59d7f2dc99f2f5deeca6c3a3b481a69c809e79d47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "abuseNotificationEmail", value)

    @builtins.property
    @jsii.member(jsii_name="adminMode")
    def admin_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adminMode"))

    @admin_mode.setter
    def admin_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195bdec48b52e6d9cfbf4810772fa746527843c488a72772a267544b1978c542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminMode", value)

    @builtins.property
    @jsii.member(jsii_name="afterSignOutPath")
    def after_sign_out_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "afterSignOutPath"))

    @after_sign_out_path.setter
    def after_sign_out_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd567d86cb605da9b8f8548b1f530d80f7b9b9cd0b38ba19e911426fd4095fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "afterSignOutPath", value)

    @builtins.property
    @jsii.member(jsii_name="afterSignUpText")
    def after_sign_up_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "afterSignUpText"))

    @after_sign_up_text.setter
    def after_sign_up_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8309494c4a00828fa1f761cc7b34698312e4a70c5471387f09494dcc286ebb34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "afterSignUpText", value)

    @builtins.property
    @jsii.member(jsii_name="akismetApiKey")
    def akismet_api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "akismetApiKey"))

    @akismet_api_key.setter
    def akismet_api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c83b3b3d12a1ac8bc0ae074c7a6df12b2cf5e11c58b42862f55d3329f6adbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "akismetApiKey", value)

    @builtins.property
    @jsii.member(jsii_name="akismetEnabled")
    def akismet_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "akismetEnabled"))

    @akismet_enabled.setter
    def akismet_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7671322f49949d14cbe4aa247a0db7bf8394eba683800a94540ea2e979e3c80a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "akismetEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="allowGroupOwnersToManageLdap")
    def allow_group_owners_to_manage_ldap(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowGroupOwnersToManageLdap"))

    @allow_group_owners_to_manage_ldap.setter
    def allow_group_owners_to_manage_ldap(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84dfaa7453e7b46ad8cb95bf68521a100600ffc077912ffb81ed306d9bbaa21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowGroupOwnersToManageLdap", value)

    @builtins.property
    @jsii.member(jsii_name="allowLocalRequestsFromSystemHooks")
    def allow_local_requests_from_system_hooks(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowLocalRequestsFromSystemHooks"))

    @allow_local_requests_from_system_hooks.setter
    def allow_local_requests_from_system_hooks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819a0565a101fa27a608fb45a0b308d41c90d0a3e84f8c78ea9d0ca27d9cb662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowLocalRequestsFromSystemHooks", value)

    @builtins.property
    @jsii.member(jsii_name="allowLocalRequestsFromWebHooksAndServices")
    def allow_local_requests_from_web_hooks_and_services(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowLocalRequestsFromWebHooksAndServices"))

    @allow_local_requests_from_web_hooks_and_services.setter
    def allow_local_requests_from_web_hooks_and_services(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2aad26fd76a2a647c3d1ee056b83a9257767a1a718efb76f2ecc932b7b32b08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowLocalRequestsFromWebHooksAndServices", value)

    @builtins.property
    @jsii.member(jsii_name="archiveBuildsInHumanReadable")
    def archive_builds_in_human_readable(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "archiveBuildsInHumanReadable"))

    @archive_builds_in_human_readable.setter
    def archive_builds_in_human_readable(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8840f70791cc0b9e9281dee33d281d12575f1be9f937b1baa22328727730ad05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveBuildsInHumanReadable", value)

    @builtins.property
    @jsii.member(jsii_name="assetProxyAllowlist")
    def asset_proxy_allowlist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "assetProxyAllowlist"))

    @asset_proxy_allowlist.setter
    def asset_proxy_allowlist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2c495be3de416225fad3461fa21ac39d66e5c6b37d70ae20ed3b47481113e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetProxyAllowlist", value)

    @builtins.property
    @jsii.member(jsii_name="assetProxyEnabled")
    def asset_proxy_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "assetProxyEnabled"))

    @asset_proxy_enabled.setter
    def asset_proxy_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4201c1ce37e8e29622940c73df81e184da0d5b62d982bebd4e33e86bac8de472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetProxyEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="assetProxySecretKey")
    def asset_proxy_secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetProxySecretKey"))

    @asset_proxy_secret_key.setter
    def asset_proxy_secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e89dce000e7e676512317012419a39595a61882c2d10c94bcdf866e8d56f756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetProxySecretKey", value)

    @builtins.property
    @jsii.member(jsii_name="assetProxyUrl")
    def asset_proxy_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assetProxyUrl"))

    @asset_proxy_url.setter
    def asset_proxy_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2abb0f27ff34622f3c92bfc3d0a19d31c62a700eaea15e05c33f919d67c4b89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assetProxyUrl", value)

    @builtins.property
    @jsii.member(jsii_name="authorizedKeysEnabled")
    def authorized_keys_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "authorizedKeysEnabled"))

    @authorized_keys_enabled.setter
    def authorized_keys_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa10c4f48c41dafd1cd1a507532f123bc24f755720fd297c2d1ac54e7db38da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedKeysEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="autoDevopsDomain")
    def auto_devops_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoDevopsDomain"))

    @auto_devops_domain.setter
    def auto_devops_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31dd3ecf27a4d8ea53ea27142ad327e4a3b461a4cd504410eadb37b8a632ddb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDevopsDomain", value)

    @builtins.property
    @jsii.member(jsii_name="autoDevopsEnabled")
    def auto_devops_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoDevopsEnabled"))

    @auto_devops_enabled.setter
    def auto_devops_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4933d4be0e623aa3573aab3139ec41641a32ca75162eb220114a2ed1609c6f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoDevopsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="automaticPurchasedStorageAllocation")
    def automatic_purchased_storage_allocation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automaticPurchasedStorageAllocation"))

    @automatic_purchased_storage_allocation.setter
    def automatic_purchased_storage_allocation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592564b8a83472647fe2fdad034afa6dcfb7ed77f51e54a32e4a35858a3f31fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticPurchasedStorageAllocation", value)

    @builtins.property
    @jsii.member(jsii_name="canCreateGroup")
    def can_create_group(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "canCreateGroup"))

    @can_create_group.setter
    def can_create_group(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0920b6de4ed161139cd2e3166c42b8ce7d8a3106925c7b962f20653f17784b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canCreateGroup", value)

    @builtins.property
    @jsii.member(jsii_name="checkNamespacePlan")
    def check_namespace_plan(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "checkNamespacePlan"))

    @check_namespace_plan.setter
    def check_namespace_plan(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf229a4e6dcdd5e58a0eef25b49ed703b33383eab38fc711107f6915a1f6fde6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkNamespacePlan", value)

    @builtins.property
    @jsii.member(jsii_name="commitEmailHostname")
    def commit_email_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commitEmailHostname"))

    @commit_email_hostname.setter
    def commit_email_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95fcd57a0126c03d2c97c489ab44087ec1daf0922510e7fcbf022f5b4b65d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commitEmailHostname", value)

    @builtins.property
    @jsii.member(jsii_name="containerExpirationPoliciesEnableHistoricEntries")
    def container_expiration_policies_enable_historic_entries(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "containerExpirationPoliciesEnableHistoricEntries"))

    @container_expiration_policies_enable_historic_entries.setter
    def container_expiration_policies_enable_historic_entries(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115eb70083b2fc47759c04b000c069744d0900ab2771bb5f36aff7c0af23db8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerExpirationPoliciesEnableHistoricEntries", value)

    @builtins.property
    @jsii.member(jsii_name="containerRegistryCleanupTagsServiceMaxListSize")
    def container_registry_cleanup_tags_service_max_list_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerRegistryCleanupTagsServiceMaxListSize"))

    @container_registry_cleanup_tags_service_max_list_size.setter
    def container_registry_cleanup_tags_service_max_list_size(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfcba578668262e63feef38b4b88f9a43b1ec287e494312dc19fd86e5b87f1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryCleanupTagsServiceMaxListSize", value)

    @builtins.property
    @jsii.member(jsii_name="containerRegistryDeleteTagsServiceTimeout")
    def container_registry_delete_tags_service_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerRegistryDeleteTagsServiceTimeout"))

    @container_registry_delete_tags_service_timeout.setter
    def container_registry_delete_tags_service_timeout(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d925706b4b7e5b1e37085138489f2fda87085a6f36c517a5a22fd739c841b81a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryDeleteTagsServiceTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="containerRegistryExpirationPoliciesCaching")
    def container_registry_expiration_policies_caching(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "containerRegistryExpirationPoliciesCaching"))

    @container_registry_expiration_policies_caching.setter
    def container_registry_expiration_policies_caching(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4dec5c9ac39e4f1905d13d66e8fe87a85f27b9e21420adc934a216dfacf71d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryExpirationPoliciesCaching", value)

    @builtins.property
    @jsii.member(jsii_name="containerRegistryExpirationPoliciesWorkerCapacity")
    def container_registry_expiration_policies_worker_capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerRegistryExpirationPoliciesWorkerCapacity"))

    @container_registry_expiration_policies_worker_capacity.setter
    def container_registry_expiration_policies_worker_capacity(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__face74d8a7ca04038c27fb02f169d96095e0d392b680eb1acc70ae0a88fd99aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryExpirationPoliciesWorkerCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="containerRegistryTokenExpireDelay")
    def container_registry_token_expire_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerRegistryTokenExpireDelay"))

    @container_registry_token_expire_delay.setter
    def container_registry_token_expire_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9fec45d9efc0cad487195a512c9017705b2e9411d6770a759afd706f952caee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryTokenExpireDelay", value)

    @builtins.property
    @jsii.member(jsii_name="deactivateDormantUsers")
    def deactivate_dormant_users(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deactivateDormantUsers"))

    @deactivate_dormant_users.setter
    def deactivate_dormant_users(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3997d0de19160dc4bce0c583821e8aa4bc125e0d7353cee051e7ac1ab5b22f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deactivateDormantUsers", value)

    @builtins.property
    @jsii.member(jsii_name="defaultArtifactsExpireIn")
    def default_artifacts_expire_in(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultArtifactsExpireIn"))

    @default_artifacts_expire_in.setter
    def default_artifacts_expire_in(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2e63ef34bd1aa1b8eabc83598fd2fde267922bb0863008a924843889404290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultArtifactsExpireIn", value)

    @builtins.property
    @jsii.member(jsii_name="defaultBranchName")
    def default_branch_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBranchName"))

    @default_branch_name.setter
    def default_branch_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe776cf51354aadc6cfd18294b7b70cd043221c8ea048f024c5e16b4fafd46b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBranchName", value)

    @builtins.property
    @jsii.member(jsii_name="defaultBranchProtection")
    def default_branch_protection(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultBranchProtection"))

    @default_branch_protection.setter
    def default_branch_protection(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d640c37b85b9259c231ac41b0fd134145b9e129843b42c7b58d22276dfe92882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBranchProtection", value)

    @builtins.property
    @jsii.member(jsii_name="defaultCiConfigPath")
    def default_ci_config_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultCiConfigPath"))

    @default_ci_config_path.setter
    def default_ci_config_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bcf51bf08869ed8d0558997d22a4330066e1d184176417ec044f4003ddc57e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultCiConfigPath", value)

    @builtins.property
    @jsii.member(jsii_name="defaultGroupVisibility")
    def default_group_visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultGroupVisibility"))

    @default_group_visibility.setter
    def default_group_visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770e619f12b4183e97641a142bbcad40a03e5bdf732402299f69270d7bfaa6c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultGroupVisibility", value)

    @builtins.property
    @jsii.member(jsii_name="defaultProjectCreation")
    def default_project_creation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultProjectCreation"))

    @default_project_creation.setter
    def default_project_creation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c79695aa028c32f5f07690434c06c42a6f524edc17e76977cedc5fee69056a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultProjectCreation", value)

    @builtins.property
    @jsii.member(jsii_name="defaultProjectsLimit")
    def default_projects_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultProjectsLimit"))

    @default_projects_limit.setter
    def default_projects_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3177a573ac67becce30b794704cf25753600eac2ef170bfea5c691dfb62a233d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultProjectsLimit", value)

    @builtins.property
    @jsii.member(jsii_name="defaultProjectVisibility")
    def default_project_visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultProjectVisibility"))

    @default_project_visibility.setter
    def default_project_visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a18e9f6275354bc8c87be7e188322df5038658b112b3acf227c1ba5870a64b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultProjectVisibility", value)

    @builtins.property
    @jsii.member(jsii_name="defaultSnippetVisibility")
    def default_snippet_visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSnippetVisibility"))

    @default_snippet_visibility.setter
    def default_snippet_visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf54ff5e1f7d8370acaa4bb080109696354c7d4c21bdacbf85b52d14e8bdb02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSnippetVisibility", value)

    @builtins.property
    @jsii.member(jsii_name="delayedGroupDeletion")
    def delayed_group_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "delayedGroupDeletion"))

    @delayed_group_deletion.setter
    def delayed_group_deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7b3cdf4d5e99efd8ba11b17c746018783cbf96a6333514dce22d838290c3fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delayedGroupDeletion", value)

    @builtins.property
    @jsii.member(jsii_name="delayedProjectDeletion")
    def delayed_project_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "delayedProjectDeletion"))

    @delayed_project_deletion.setter
    def delayed_project_deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4753a5c192df5e7d748e92ced9cb38c4c476e8bde079c552e700ae4ea6d379f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delayedProjectDeletion", value)

    @builtins.property
    @jsii.member(jsii_name="deleteInactiveProjects")
    def delete_inactive_projects(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteInactiveProjects"))

    @delete_inactive_projects.setter
    def delete_inactive_projects(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0375fefb760d2f45930b6562c586e16207418940810b437061feff39741820f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteInactiveProjects", value)

    @builtins.property
    @jsii.member(jsii_name="deletionAdjournedPeriod")
    def deletion_adjourned_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deletionAdjournedPeriod"))

    @deletion_adjourned_period.setter
    def deletion_adjourned_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0ece0afbd124e339c95bcb4916833451dcbe7c4cd0152231ddb77ede13dbe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionAdjournedPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="diffMaxFiles")
    def diff_max_files(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diffMaxFiles"))

    @diff_max_files.setter
    def diff_max_files(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f9a44022d1b6548bc334d6ae36ec326ee1aac922937a0d831e26c8c0288a0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diffMaxFiles", value)

    @builtins.property
    @jsii.member(jsii_name="diffMaxLines")
    def diff_max_lines(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diffMaxLines"))

    @diff_max_lines.setter
    def diff_max_lines(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a4206909aecdf774bd399b510a5fa7e2cff0cb51c723f6d63fd9ecb7f7be7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diffMaxLines", value)

    @builtins.property
    @jsii.member(jsii_name="diffMaxPatchBytes")
    def diff_max_patch_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diffMaxPatchBytes"))

    @diff_max_patch_bytes.setter
    def diff_max_patch_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50cc06f90fd4a7badd51e9f60ac48c58fa8af43731bac5068b1e71dccbd97b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diffMaxPatchBytes", value)

    @builtins.property
    @jsii.member(jsii_name="disabledOauthSignInSources")
    def disabled_oauth_sign_in_sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "disabledOauthSignInSources"))

    @disabled_oauth_sign_in_sources.setter
    def disabled_oauth_sign_in_sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a778692cf8d526261df878c730ef2966872965488222d43646ca6f8611e569e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabledOauthSignInSources", value)

    @builtins.property
    @jsii.member(jsii_name="disableFeedToken")
    def disable_feed_token(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableFeedToken"))

    @disable_feed_token.setter
    def disable_feed_token(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a376790bb8980fb468f1e2939bae26fe212184ed8944d6edb2fb5b520f68521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableFeedToken", value)

    @builtins.property
    @jsii.member(jsii_name="dnsRebindingProtectionEnabled")
    def dns_rebinding_protection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dnsRebindingProtectionEnabled"))

    @dns_rebinding_protection_enabled.setter
    def dns_rebinding_protection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450598c234758128f504b9961c0ce8c488203822cefb999e53a23754e86afd40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsRebindingProtectionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="domainAllowlist")
    def domain_allowlist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainAllowlist"))

    @domain_allowlist.setter
    def domain_allowlist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b50d3c4102ccbad36e4c9b711bb1f9f9768cc8311b38ef88044cebdb7d0996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainAllowlist", value)

    @builtins.property
    @jsii.member(jsii_name="domainDenylist")
    def domain_denylist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainDenylist"))

    @domain_denylist.setter
    def domain_denylist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ddd96cde6e59c3e7e40a8ef39a4e9ff9aa7689ad0d8e7b27704584206d5a76a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainDenylist", value)

    @builtins.property
    @jsii.member(jsii_name="domainDenylistEnabled")
    def domain_denylist_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "domainDenylistEnabled"))

    @domain_denylist_enabled.setter
    def domain_denylist_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15afdf3d163ea4b5b68f9dd4ca663435f35159b56401972b7d18d31ee70b7105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainDenylistEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="dsaKeyRestriction")
    def dsa_key_restriction(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dsaKeyRestriction"))

    @dsa_key_restriction.setter
    def dsa_key_restriction(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab197cbafd4e4b5009ffdf1e1ecbfd420ed7c37b1027cb2cd23e003c47718727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dsaKeyRestriction", value)

    @builtins.property
    @jsii.member(jsii_name="ecdsaKeyRestriction")
    def ecdsa_key_restriction(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ecdsaKeyRestriction"))

    @ecdsa_key_restriction.setter
    def ecdsa_key_restriction(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb025c8b906a15a50054be160d174e05d1c3cc51dc2d1e3da2fddf145e6f1f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ecdsaKeyRestriction", value)

    @builtins.property
    @jsii.member(jsii_name="ecdsaSkKeyRestriction")
    def ecdsa_sk_key_restriction(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ecdsaSkKeyRestriction"))

    @ecdsa_sk_key_restriction.setter
    def ecdsa_sk_key_restriction(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__705c7d064f8d0fd0dde993fe2dfa25f6eb37b60307730e0e42ebda57cf50152c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ecdsaSkKeyRestriction", value)

    @builtins.property
    @jsii.member(jsii_name="ed25519KeyRestriction")
    def ed25519_key_restriction(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ed25519KeyRestriction"))

    @ed25519_key_restriction.setter
    def ed25519_key_restriction(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552755c563ff21bfc35227644de0d4f14e293501716c97aa6acf86fd83f4ee1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ed25519KeyRestriction", value)

    @builtins.property
    @jsii.member(jsii_name="ed25519SkKeyRestriction")
    def ed25519_sk_key_restriction(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ed25519SkKeyRestriction"))

    @ed25519_sk_key_restriction.setter
    def ed25519_sk_key_restriction(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf8c20f7c66ae2affe14550155718d3b7693de53e84afa9220d278c0ec2b6bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ed25519SkKeyRestriction", value)

    @builtins.property
    @jsii.member(jsii_name="eksAccessKeyId")
    def eks_access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eksAccessKeyId"))

    @eks_access_key_id.setter
    def eks_access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55412fdfe87900505c2561d4b719c3b9eb6c05964d0cc3405eb9c1961ff51df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eksAccessKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="eksAccountId")
    def eks_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eksAccountId"))

    @eks_account_id.setter
    def eks_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f30e89051cf0ad9868296cb2009750b06f24cac91c9821549e393cc0a1bc83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eksAccountId", value)

    @builtins.property
    @jsii.member(jsii_name="eksIntegrationEnabled")
    def eks_integration_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "eksIntegrationEnabled"))

    @eks_integration_enabled.setter
    def eks_integration_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387d99cb2c804bbf9d20b6f822c562dfcd58377894b7946a6cc2d3d28f805532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eksIntegrationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="eksSecretAccessKey")
    def eks_secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eksSecretAccessKey"))

    @eks_secret_access_key.setter
    def eks_secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a712cf93c8611d44d01310729b5eaa8173b5742f78e509da7cffe17c037e091f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eksSecretAccessKey", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchAws")
    def elasticsearch_aws(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "elasticsearchAws"))

    @elasticsearch_aws.setter
    def elasticsearch_aws(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65bf35ce107ac03a8aec2608fe67c0e9c13c2f75f92ec64b913d2a0cae4f8407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchAws", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchAwsAccessKey")
    def elasticsearch_aws_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchAwsAccessKey"))

    @elasticsearch_aws_access_key.setter
    def elasticsearch_aws_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5988e85a7db28134cf598d5d5b21322051b897a708afb5c8589bd6b3f411644a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchAwsAccessKey", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchAwsRegion")
    def elasticsearch_aws_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchAwsRegion"))

    @elasticsearch_aws_region.setter
    def elasticsearch_aws_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acdde3bda48f94b4f33e28fd2fc4adfaebf5d00e48719eac504c5a79811d88dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchAwsRegion", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchAwsSecretAccessKey")
    def elasticsearch_aws_secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchAwsSecretAccessKey"))

    @elasticsearch_aws_secret_access_key.setter
    def elasticsearch_aws_secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5958bfcea1c56e0ee3b7037c1e49ff1f2c4f2f7e4a283f143a795e9d7fb76945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchAwsSecretAccessKey", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchIndexedFieldLengthLimit")
    def elasticsearch_indexed_field_length_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "elasticsearchIndexedFieldLengthLimit"))

    @elasticsearch_indexed_field_length_limit.setter
    def elasticsearch_indexed_field_length_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04ff99674734cfa0337f9172ec4cae02c7618a259e3804dc2550230b46d3452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchIndexedFieldLengthLimit", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchIndexedFileSizeLimitKb")
    def elasticsearch_indexed_file_size_limit_kb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "elasticsearchIndexedFileSizeLimitKb"))

    @elasticsearch_indexed_file_size_limit_kb.setter
    def elasticsearch_indexed_file_size_limit_kb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c768db788363ed0dd6d8a4d68d0480e0767273ba0081d2e0e3146f99fa78e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchIndexedFileSizeLimitKb", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchIndexing")
    def elasticsearch_indexing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "elasticsearchIndexing"))

    @elasticsearch_indexing.setter
    def elasticsearch_indexing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02abe694f0393b81a3d248ee331bde1adef195023a8e81a3842b3b96dd2c911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchIndexing", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchLimitIndexing")
    def elasticsearch_limit_indexing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "elasticsearchLimitIndexing"))

    @elasticsearch_limit_indexing.setter
    def elasticsearch_limit_indexing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b695737f8560b76821d03e56aba40dbb47b0e672dbbb53a1a502031b41d5eef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchLimitIndexing", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchMaxBulkConcurrency")
    def elasticsearch_max_bulk_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "elasticsearchMaxBulkConcurrency"))

    @elasticsearch_max_bulk_concurrency.setter
    def elasticsearch_max_bulk_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e33a047821ea4d809285be7c8bc810fcc4e927e19c8f5e5a20f263a6129d514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchMaxBulkConcurrency", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchMaxBulkSizeMb")
    def elasticsearch_max_bulk_size_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "elasticsearchMaxBulkSizeMb"))

    @elasticsearch_max_bulk_size_mb.setter
    def elasticsearch_max_bulk_size_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c70f0a118a2a498f0371556d5e93c35ccf9b198cbc640362481c73c98aabd9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchMaxBulkSizeMb", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchNamespaceIds")
    def elasticsearch_namespace_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "elasticsearchNamespaceIds"))

    @elasticsearch_namespace_ids.setter
    def elasticsearch_namespace_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ae98cfa0839840b4ad2fe780611f18aab41d42e0d59cf8d5028d34ea4cb949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchNamespaceIds", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchPassword")
    def elasticsearch_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchPassword"))

    @elasticsearch_password.setter
    def elasticsearch_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e769e82f0cb20b47197bf9df2818e9310775a6917c34c13e8900e4867d681605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchPassword", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchProjectIds")
    def elasticsearch_project_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "elasticsearchProjectIds"))

    @elasticsearch_project_ids.setter
    def elasticsearch_project_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce45bb29b98e15069d4a4bc38b5cac1ee760f62810626b72eccb26ccba96c8cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchProjectIds", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchSearch")
    def elasticsearch_search(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "elasticsearchSearch"))

    @elasticsearch_search.setter
    def elasticsearch_search(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44348a62f1cf6bf7200285c5fae5fcecfb15c4f244553b79bc85b36c7b6da2de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchSearch", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchUrl")
    def elasticsearch_url(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "elasticsearchUrl"))

    @elasticsearch_url.setter
    def elasticsearch_url(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e140a909ccdb09c393ade4e757936c89fdc566e8f42e515d379de9d614fa8235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchUrl", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchUsername")
    def elasticsearch_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticsearchUsername"))

    @elasticsearch_username.setter
    def elasticsearch_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de63b347ccf4a9ad2e023151f9f55cf2cbbe76f985197da4bd17e22e65d1732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchUsername", value)

    @builtins.property
    @jsii.member(jsii_name="emailAdditionalText")
    def email_additional_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailAdditionalText"))

    @email_additional_text.setter
    def email_additional_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c916d7a49303777495f68851d720b3c308dec7b13a0cdccf3f0270737aa8a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAdditionalText", value)

    @builtins.property
    @jsii.member(jsii_name="emailAuthorInBody")
    def email_author_in_body(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "emailAuthorInBody"))

    @email_author_in_body.setter
    def email_author_in_body(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e310c42683084bb7d23e7e069d8855f371208fb304a84dca0a92af75a18d209e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAuthorInBody", value)

    @builtins.property
    @jsii.member(jsii_name="enabledGitAccessProtocol")
    def enabled_git_access_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enabledGitAccessProtocol"))

    @enabled_git_access_protocol.setter
    def enabled_git_access_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787d905ca740f6b5019152939d46c361e29ae1e8fca728fe78e9cfd02eacdca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabledGitAccessProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="enforceNamespaceStorageLimit")
    def enforce_namespace_storage_limit(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforceNamespaceStorageLimit"))

    @enforce_namespace_storage_limit.setter
    def enforce_namespace_storage_limit(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fd57d43c0fc614ed129dc54b298490f49716c4a4cd0480b10d7701548a36ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceNamespaceStorageLimit", value)

    @builtins.property
    @jsii.member(jsii_name="enforceTerms")
    def enforce_terms(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforceTerms"))

    @enforce_terms.setter
    def enforce_terms(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b573a1476cae3f2874b458cb63f2c134f8d938fffe25437e93e1ed149a2744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceTerms", value)

    @builtins.property
    @jsii.member(jsii_name="externalAuthClientCert")
    def external_auth_client_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAuthClientCert"))

    @external_auth_client_cert.setter
    def external_auth_client_cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6490f0b5a8d251fd84eda6637c2d824bcad132dd843c30458c6fd6eee73afd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAuthClientCert", value)

    @builtins.property
    @jsii.member(jsii_name="externalAuthClientKey")
    def external_auth_client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAuthClientKey"))

    @external_auth_client_key.setter
    def external_auth_client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330a3fa19856a8601ae5509a92683b91b0ec15a312d64646c934f588df3f2ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAuthClientKey", value)

    @builtins.property
    @jsii.member(jsii_name="externalAuthClientKeyPass")
    def external_auth_client_key_pass(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAuthClientKeyPass"))

    @external_auth_client_key_pass.setter
    def external_auth_client_key_pass(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb56d170ac04bc248dfb8cff82d12d687e76cce8e2b0a1cbdfd5adc347b6aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAuthClientKeyPass", value)

    @builtins.property
    @jsii.member(jsii_name="externalAuthorizationServiceDefaultLabel")
    def external_authorization_service_default_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAuthorizationServiceDefaultLabel"))

    @external_authorization_service_default_label.setter
    def external_authorization_service_default_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18564d64243ad92d1364832c8a5043424c4d81cfd49f47099aa113837e31034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAuthorizationServiceDefaultLabel", value)

    @builtins.property
    @jsii.member(jsii_name="externalAuthorizationServiceEnabled")
    def external_authorization_service_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "externalAuthorizationServiceEnabled"))

    @external_authorization_service_enabled.setter
    def external_authorization_service_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0454f4a03e4fcf0936b4539192aab530c67d6deee47d6bcc11e29c3c0f00e50d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAuthorizationServiceEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="externalAuthorizationServiceTimeout")
    def external_authorization_service_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "externalAuthorizationServiceTimeout"))

    @external_authorization_service_timeout.setter
    def external_authorization_service_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe83534f7fe96ecc9e0db6b169f48a1ed63d5d2aff664213b058112f60bd5c40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAuthorizationServiceTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="externalAuthorizationServiceUrl")
    def external_authorization_service_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAuthorizationServiceUrl"))

    @external_authorization_service_url.setter
    def external_authorization_service_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c09b3b061e0e0fd5374c29c4049e7746740c59cb51c86f6320a868c487ad6fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAuthorizationServiceUrl", value)

    @builtins.property
    @jsii.member(jsii_name="externalPipelineValidationServiceTimeout")
    def external_pipeline_validation_service_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "externalPipelineValidationServiceTimeout"))

    @external_pipeline_validation_service_timeout.setter
    def external_pipeline_validation_service_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd6b8ff1ed4b405e9b419393b014aab2e5cb2af137c4e81fa08b6b5253033245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalPipelineValidationServiceTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="externalPipelineValidationServiceToken")
    def external_pipeline_validation_service_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalPipelineValidationServiceToken"))

    @external_pipeline_validation_service_token.setter
    def external_pipeline_validation_service_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d5aeabe8c0c072bca3fe32f580d8f88a004a0064f238ecc574d982210daa8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalPipelineValidationServiceToken", value)

    @builtins.property
    @jsii.member(jsii_name="externalPipelineValidationServiceUrl")
    def external_pipeline_validation_service_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalPipelineValidationServiceUrl"))

    @external_pipeline_validation_service_url.setter
    def external_pipeline_validation_service_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d969fb2b07b3785bea4f912b48e9b493a6830388184ed5b90f1eb231722822d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalPipelineValidationServiceUrl", value)

    @builtins.property
    @jsii.member(jsii_name="fileTemplateProjectId")
    def file_template_project_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fileTemplateProjectId"))

    @file_template_project_id.setter
    def file_template_project_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8784fe54b256147528d32ddb2c6389566d9cae80b927cd2a94bc283e4007726a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileTemplateProjectId", value)

    @builtins.property
    @jsii.member(jsii_name="firstDayOfWeek")
    def first_day_of_week(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "firstDayOfWeek"))

    @first_day_of_week.setter
    def first_day_of_week(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9bc7a29cdb363fd5e46c1ba709c34b001d7c534303df0ce56b2019d9e917cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstDayOfWeek", value)

    @builtins.property
    @jsii.member(jsii_name="geoNodeAllowedIps")
    def geo_node_allowed_ips(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geoNodeAllowedIps"))

    @geo_node_allowed_ips.setter
    def geo_node_allowed_ips(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc01376258c5e7c4df6b4d0fe98ac904cdf73fa424c04fc226edc9283b4f24c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geoNodeAllowedIps", value)

    @builtins.property
    @jsii.member(jsii_name="geoStatusTimeout")
    def geo_status_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "geoStatusTimeout"))

    @geo_status_timeout.setter
    def geo_status_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499c824787099b1e6cbdeff5b74450c0fc2fd4917c5edea7ed11e887b8f89433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geoStatusTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="gitalyTimeoutDefault")
    def gitaly_timeout_default(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gitalyTimeoutDefault"))

    @gitaly_timeout_default.setter
    def gitaly_timeout_default(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a66f7325e4438208961507bf9498e27ad1ae802c70a3f2fea831a0709095645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitalyTimeoutDefault", value)

    @builtins.property
    @jsii.member(jsii_name="gitalyTimeoutFast")
    def gitaly_timeout_fast(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gitalyTimeoutFast"))

    @gitaly_timeout_fast.setter
    def gitaly_timeout_fast(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48127944d47f172c3b7cee2fc224db36e23e4d50fa6b7d6e07d0ccc71cc4b993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitalyTimeoutFast", value)

    @builtins.property
    @jsii.member(jsii_name="gitalyTimeoutMedium")
    def gitaly_timeout_medium(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gitalyTimeoutMedium"))

    @gitaly_timeout_medium.setter
    def gitaly_timeout_medium(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad53277ccef59b9e7591a3105cef18759bb017c1dcc1bb6e78e14e87d554093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitalyTimeoutMedium", value)

    @builtins.property
    @jsii.member(jsii_name="gitRateLimitUsersAllowlist")
    def git_rate_limit_users_allowlist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gitRateLimitUsersAllowlist"))

    @git_rate_limit_users_allowlist.setter
    def git_rate_limit_users_allowlist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8166c4efecdb3412ae1322965ac9a16219bf431bbeea984f4cc4240214267bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitRateLimitUsersAllowlist", value)

    @builtins.property
    @jsii.member(jsii_name="gitTwoFactorSessionExpiry")
    def git_two_factor_session_expiry(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gitTwoFactorSessionExpiry"))

    @git_two_factor_session_expiry.setter
    def git_two_factor_session_expiry(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6fae00b4a1da37e525c1f45b494b5cb5284b478c5b9d88f534deec6e0090761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitTwoFactorSessionExpiry", value)

    @builtins.property
    @jsii.member(jsii_name="grafanaEnabled")
    def grafana_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "grafanaEnabled"))

    @grafana_enabled.setter
    def grafana_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5964874a644a381707374474460148ed7236f5104f983ee33ea49d20dabbf776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grafanaEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="grafanaUrl")
    def grafana_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grafanaUrl"))

    @grafana_url.setter
    def grafana_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fced3fc6ceb24294ac04fab81144c96de91917b796143b9d888f4558dc05372c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grafanaUrl", value)

    @builtins.property
    @jsii.member(jsii_name="gravatarEnabled")
    def gravatar_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "gravatarEnabled"))

    @gravatar_enabled.setter
    def gravatar_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809394eff63b48adf2c8875c3792c06a6197a2cd8aece30ff78fd4889409bea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gravatarEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="groupOwnersCanManageDefaultBranchProtection")
    def group_owners_can_manage_default_branch_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "groupOwnersCanManageDefaultBranchProtection"))

    @group_owners_can_manage_default_branch_protection.setter
    def group_owners_can_manage_default_branch_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0c67663346c031d82f82718d574041fc9aa1f7f1d403b71cf48979e556215f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupOwnersCanManageDefaultBranchProtection", value)

    @builtins.property
    @jsii.member(jsii_name="hashedStorageEnabled")
    def hashed_storage_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hashedStorageEnabled"))

    @hashed_storage_enabled.setter
    def hashed_storage_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84edcb6476c53c14784c1ad7ee1b4c0775958079d4328352ec22af0ec0f7c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashedStorageEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="helpPageHideCommercialContent")
    def help_page_hide_commercial_content(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "helpPageHideCommercialContent"))

    @help_page_hide_commercial_content.setter
    def help_page_hide_commercial_content(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e593ec055d08cda6eb2a8d8ee899d1ed63a939ebdca328fd53414e4227ef7a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "helpPageHideCommercialContent", value)

    @builtins.property
    @jsii.member(jsii_name="helpPageSupportUrl")
    def help_page_support_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "helpPageSupportUrl"))

    @help_page_support_url.setter
    def help_page_support_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc2a9bdf24b1f22a3d15bcc062431abec9263a0da2f21ff17d67a3dd6805a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "helpPageSupportUrl", value)

    @builtins.property
    @jsii.member(jsii_name="helpPageText")
    def help_page_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "helpPageText"))

    @help_page_text.setter
    def help_page_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdf4048b21a579af2ed5f52791b046e56dd889f549dc04d2a32b98022348545c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "helpPageText", value)

    @builtins.property
    @jsii.member(jsii_name="helpText")
    def help_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "helpText"))

    @help_text.setter
    def help_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1da8f55f6f127d0588f186ce8ef0e4025501cb09b636fa2e273376dc2ee9a1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "helpText", value)

    @builtins.property
    @jsii.member(jsii_name="hideThirdPartyOffers")
    def hide_third_party_offers(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hideThirdPartyOffers"))

    @hide_third_party_offers.setter
    def hide_third_party_offers(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8efeb701b5b439a39622be0aca7ab31fef0316c8bd500b1362b92f2846d7c42c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hideThirdPartyOffers", value)

    @builtins.property
    @jsii.member(jsii_name="homePageUrl")
    def home_page_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "homePageUrl"))

    @home_page_url.setter
    def home_page_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0201ed2784edea2b985f09770053efab6f583be18ca1b12a123a839fe975274a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homePageUrl", value)

    @builtins.property
    @jsii.member(jsii_name="housekeepingEnabled")
    def housekeeping_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "housekeepingEnabled"))

    @housekeeping_enabled.setter
    def housekeeping_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95d6aa0795ca71d4ff8fa1e51f13ef40d2ee0855f4159c0165aa6705fa408f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "housekeepingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="housekeepingFullRepackPeriod")
    def housekeeping_full_repack_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "housekeepingFullRepackPeriod"))

    @housekeeping_full_repack_period.setter
    def housekeeping_full_repack_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5d20cc9f2714b91d85df4f39c416b3523f98060d2de9cde9bb3486720a510c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "housekeepingFullRepackPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="housekeepingGcPeriod")
    def housekeeping_gc_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "housekeepingGcPeriod"))

    @housekeeping_gc_period.setter
    def housekeeping_gc_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69e33710fd6608daef93492bfc94e2e9545c54c8e54f14aa6d03130df19de4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "housekeepingGcPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="housekeepingIncrementalRepackPeriod")
    def housekeeping_incremental_repack_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "housekeepingIncrementalRepackPeriod"))

    @housekeeping_incremental_repack_period.setter
    def housekeeping_incremental_repack_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633463f0acf790baf9dcaef91fb26149c83385d5ed70655354c653b1b51e9439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "housekeepingIncrementalRepackPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="htmlEmailsEnabled")
    def html_emails_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "htmlEmailsEnabled"))

    @html_emails_enabled.setter
    def html_emails_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbee57fdacdc5368e7e8d7d3d6fd32438bfddaaed7dd00ce3c5144d2d417a8aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "htmlEmailsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8a49360754d6cf895e3345343085f9860e5a9636dd9237e304356d6b8889d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="importSources")
    def import_sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "importSources"))

    @import_sources.setter
    def import_sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ade0be50630d270b560bb453cc433117ae1a4ac477dfd40051e6a823fe84641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importSources", value)

    @builtins.property
    @jsii.member(jsii_name="inactiveProjectsDeleteAfterMonths")
    def inactive_projects_delete_after_months(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "inactiveProjectsDeleteAfterMonths"))

    @inactive_projects_delete_after_months.setter
    def inactive_projects_delete_after_months(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233e1a9116cbf60b4bde135bff521ee4bc63b26e4e090d09a916cf836225f887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inactiveProjectsDeleteAfterMonths", value)

    @builtins.property
    @jsii.member(jsii_name="inactiveProjectsMinSizeMb")
    def inactive_projects_min_size_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "inactiveProjectsMinSizeMb"))

    @inactive_projects_min_size_mb.setter
    def inactive_projects_min_size_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce8761e77747d51ca1dd7938ff5851739a336801a6bf6b79b2dbc178db22ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inactiveProjectsMinSizeMb", value)

    @builtins.property
    @jsii.member(jsii_name="inactiveProjectsSendWarningEmailAfterMonths")
    def inactive_projects_send_warning_email_after_months(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "inactiveProjectsSendWarningEmailAfterMonths"))

    @inactive_projects_send_warning_email_after_months.setter
    def inactive_projects_send_warning_email_after_months(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e05afad5201e034086d5a533073271d3875a4a7e14849ceef2ba977e3be7fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inactiveProjectsSendWarningEmailAfterMonths", value)

    @builtins.property
    @jsii.member(jsii_name="inProductMarketingEmailsEnabled")
    def in_product_marketing_emails_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inProductMarketingEmailsEnabled"))

    @in_product_marketing_emails_enabled.setter
    def in_product_marketing_emails_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51e7362b701e82645b4676f0c507e9c3aa0fee7a48cfa4fad0e7ed03b86e0e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inProductMarketingEmailsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="invisibleCaptchaEnabled")
    def invisible_captcha_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invisibleCaptchaEnabled"))

    @invisible_captcha_enabled.setter
    def invisible_captcha_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b86e1030c11cfe22d5e5a9762872e77f401dff953f25495f321cc84ffebde6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invisibleCaptchaEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="issuesCreateLimit")
    def issues_create_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "issuesCreateLimit"))

    @issues_create_limit.setter
    def issues_create_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1466c48781cd7981dc59a6a4d5b777161dfd2d23db5daa55c606865678b7a4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuesCreateLimit", value)

    @builtins.property
    @jsii.member(jsii_name="keepLatestArtifact")
    def keep_latest_artifact(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keepLatestArtifact"))

    @keep_latest_artifact.setter
    def keep_latest_artifact(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__280eed4e3e860523a535f85509b7015d776d64906b67422d1d4d0bef2f5c624c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepLatestArtifact", value)

    @builtins.property
    @jsii.member(jsii_name="localMarkdownVersion")
    def local_markdown_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localMarkdownVersion"))

    @local_markdown_version.setter
    def local_markdown_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ab352eae928e05a96c1ebdb6758bd408ceee399e1d8cacaf083bd51d9ad592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localMarkdownVersion", value)

    @builtins.property
    @jsii.member(jsii_name="mailgunEventsEnabled")
    def mailgun_events_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mailgunEventsEnabled"))

    @mailgun_events_enabled.setter
    def mailgun_events_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c928949d2d694927da29424c7060ff39687b894033c5e4b46a30bf1010d540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mailgunEventsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="mailgunSigningKey")
    def mailgun_signing_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mailgunSigningKey"))

    @mailgun_signing_key.setter
    def mailgun_signing_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e581dbaa2aa7c15b20414962cedacbd64d7a3f67e70c851b45da5e3d444e477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mailgunSigningKey", value)

    @builtins.property
    @jsii.member(jsii_name="maintenanceMode")
    def maintenance_mode(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "maintenanceMode"))

    @maintenance_mode.setter
    def maintenance_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff23cccbb7342bfffd0f76dc590f30ea77e9efc93135ee8090b22d40161daf64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceMode", value)

    @builtins.property
    @jsii.member(jsii_name="maintenanceModeMessage")
    def maintenance_mode_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceModeMessage"))

    @maintenance_mode_message.setter
    def maintenance_mode_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c43a8656427a874d37c72f8ec75a6c6c2f8a0cc204e1c53e5f363fc992237c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceModeMessage", value)

    @builtins.property
    @jsii.member(jsii_name="maxArtifactsSize")
    def max_artifacts_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxArtifactsSize"))

    @max_artifacts_size.setter
    def max_artifacts_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d633ee1fcf7403108b14df4f8aa90c895549d1165d0a554c400c5f90d2250d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxArtifactsSize", value)

    @builtins.property
    @jsii.member(jsii_name="maxAttachmentSize")
    def max_attachment_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAttachmentSize"))

    @max_attachment_size.setter
    def max_attachment_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bef462704cf1877a2d4e9873724ea79d6dc9e68c61bd4c999bc1311eb56395e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttachmentSize", value)

    @builtins.property
    @jsii.member(jsii_name="maxExportSize")
    def max_export_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxExportSize"))

    @max_export_size.setter
    def max_export_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a0a140ac67114e5287a31cd4f63056d3591cd8baa6d3a6a1880b115de1a61e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxExportSize", value)

    @builtins.property
    @jsii.member(jsii_name="maxImportSize")
    def max_import_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxImportSize"))

    @max_import_size.setter
    def max_import_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3436060588fc35e237d78eea35a1ff75bbef64667f28c9c2f83a42ab14613ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxImportSize", value)

    @builtins.property
    @jsii.member(jsii_name="maxNumberOfRepositoryDownloads")
    def max_number_of_repository_downloads(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNumberOfRepositoryDownloads"))

    @max_number_of_repository_downloads.setter
    def max_number_of_repository_downloads(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e483dc8bd5b2b30950be8b6cbed4e90fa7c6cd46498f87976cde39c58a94441c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNumberOfRepositoryDownloads", value)

    @builtins.property
    @jsii.member(jsii_name="maxNumberOfRepositoryDownloadsWithinTimePeriod")
    def max_number_of_repository_downloads_within_time_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNumberOfRepositoryDownloadsWithinTimePeriod"))

    @max_number_of_repository_downloads_within_time_period.setter
    def max_number_of_repository_downloads_within_time_period(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f42d43c863bb180a8f7703965859bf6aa10088437a1af8faad4e552b8fd38c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNumberOfRepositoryDownloadsWithinTimePeriod", value)

    @builtins.property
    @jsii.member(jsii_name="maxPagesSize")
    def max_pages_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPagesSize"))

    @max_pages_size.setter
    def max_pages_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__022d9760ba4f8bbff894732c80ab690d64fb08d132d0c59349b1537bce595f67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPagesSize", value)

    @builtins.property
    @jsii.member(jsii_name="maxPersonalAccessTokenLifetime")
    def max_personal_access_token_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPersonalAccessTokenLifetime"))

    @max_personal_access_token_lifetime.setter
    def max_personal_access_token_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbeae9e2d398e54634c5dd753121c04ecb9c4e80034408439454e1f320a40072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPersonalAccessTokenLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxSshKeyLifetime")
    def max_ssh_key_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSshKeyLifetime"))

    @max_ssh_key_lifetime.setter
    def max_ssh_key_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7c7c11f12d1386c042ff21f0b6eb6d849cbafc0a1de6894992b15feeec65203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSshKeyLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="metricsMethodCallThreshold")
    def metrics_method_call_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsMethodCallThreshold"))

    @metrics_method_call_threshold.setter
    def metrics_method_call_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5890cb97900107e7449e805c7ebbb801080218a9cd20691ed8d7080e6c42feaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsMethodCallThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="mirrorAvailable")
    def mirror_available(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mirrorAvailable"))

    @mirror_available.setter
    def mirror_available(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6f0e3d591514f3b17ccd956a7bad812afd504c9f14aebc4b0e62c5522c5d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirrorAvailable", value)

    @builtins.property
    @jsii.member(jsii_name="mirrorCapacityThreshold")
    def mirror_capacity_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mirrorCapacityThreshold"))

    @mirror_capacity_threshold.setter
    def mirror_capacity_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b0a0d8d07f884b647e68711ee77b64421d870ffe53819a33cef4c6da32eb61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirrorCapacityThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="mirrorMaxCapacity")
    def mirror_max_capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mirrorMaxCapacity"))

    @mirror_max_capacity.setter
    def mirror_max_capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10daf1a08ba773ad94f112d86d5f2cbdaef84e1922def74f1516f79259d2ed16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirrorMaxCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="mirrorMaxDelay")
    def mirror_max_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mirrorMaxDelay"))

    @mirror_max_delay.setter
    def mirror_max_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4982493e67f9f4073fe2ce75e3559ea0272cced56f0caf2e0ca2f2b9c4cbe3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mirrorMaxDelay", value)

    @builtins.property
    @jsii.member(jsii_name="npmPackageRequestsForwarding")
    def npm_package_requests_forwarding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "npmPackageRequestsForwarding"))

    @npm_package_requests_forwarding.setter
    def npm_package_requests_forwarding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0fe443163b5f619da39990b705583f71202674a40f17c1268c3aabf14172d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "npmPackageRequestsForwarding", value)

    @builtins.property
    @jsii.member(jsii_name="outboundLocalRequestsWhitelist")
    def outbound_local_requests_whitelist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outboundLocalRequestsWhitelist"))

    @outbound_local_requests_whitelist.setter
    def outbound_local_requests_whitelist(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3257bed68a1b35232d7b1713f648d4ccb2f20e6ff92e8b0da92418f493fc84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundLocalRequestsWhitelist", value)

    @builtins.property
    @jsii.member(jsii_name="packageRegistryCleanupPoliciesWorkerCapacity")
    def package_registry_cleanup_policies_worker_capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "packageRegistryCleanupPoliciesWorkerCapacity"))

    @package_registry_cleanup_policies_worker_capacity.setter
    def package_registry_cleanup_policies_worker_capacity(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a253defc20a7d050ae889ba8b6b367bc3e668c16916fba48bd1c506d52dedd31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packageRegistryCleanupPoliciesWorkerCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="pagesDomainVerificationEnabled")
    def pages_domain_verification_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pagesDomainVerificationEnabled"))

    @pages_domain_verification_enabled.setter
    def pages_domain_verification_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac07ff1e54d83f7985a327525dc69be6800e7b45c3fb004f161a922bfe17be91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pagesDomainVerificationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="passwordAuthenticationEnabledForGit")
    def password_authentication_enabled_for_git(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordAuthenticationEnabledForGit"))

    @password_authentication_enabled_for_git.setter
    def password_authentication_enabled_for_git(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0376e5766ce583312bff595c953665200e534c967ddedbe8c06861b965a4e290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordAuthenticationEnabledForGit", value)

    @builtins.property
    @jsii.member(jsii_name="passwordAuthenticationEnabledForWeb")
    def password_authentication_enabled_for_web(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordAuthenticationEnabledForWeb"))

    @password_authentication_enabled_for_web.setter
    def password_authentication_enabled_for_web(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__571ec836c876cd5c029ec61d9382428136763fd9fa3592d6c1da5bb38ca6d658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordAuthenticationEnabledForWeb", value)

    @builtins.property
    @jsii.member(jsii_name="passwordLowercaseRequired")
    def password_lowercase_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordLowercaseRequired"))

    @password_lowercase_required.setter
    def password_lowercase_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__289f13380b64aff9610a79a6c90becd7a22cf64247a314d0b618aef759b56082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordLowercaseRequired", value)

    @builtins.property
    @jsii.member(jsii_name="passwordNumberRequired")
    def password_number_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordNumberRequired"))

    @password_number_required.setter
    def password_number_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec6c9be6e12370cc63fd6d468b21e619e03704bf4429e374e4759a9919eb3cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordNumberRequired", value)

    @builtins.property
    @jsii.member(jsii_name="passwordSymbolRequired")
    def password_symbol_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordSymbolRequired"))

    @password_symbol_required.setter
    def password_symbol_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2dfbd350eebc8bf4637d428856bc50cd4ebc6e7238dbeff086e4f389a3b5b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordSymbolRequired", value)

    @builtins.property
    @jsii.member(jsii_name="passwordUppercaseRequired")
    def password_uppercase_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordUppercaseRequired"))

    @password_uppercase_required.setter
    def password_uppercase_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fed18e1fba5fc202a0b461a80ed32a7539382ca90bf1cfaff63041788ae4cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordUppercaseRequired", value)

    @builtins.property
    @jsii.member(jsii_name="performanceBarAllowedGroupPath")
    def performance_bar_allowed_group_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "performanceBarAllowedGroupPath"))

    @performance_bar_allowed_group_path.setter
    def performance_bar_allowed_group_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c22478ec8dfc35d8e9ed9a35893ab9a6d060a5a2e933eda14bfe6c423b9482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "performanceBarAllowedGroupPath", value)

    @builtins.property
    @jsii.member(jsii_name="personalAccessTokenPrefix")
    def personal_access_token_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "personalAccessTokenPrefix"))

    @personal_access_token_prefix.setter
    def personal_access_token_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754068b55498b76cc1ea5c64d92b3243346e713f99bcabe4fe538eeec99bb28b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "personalAccessTokenPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="pipelineLimitPerProjectUserSha")
    def pipeline_limit_per_project_user_sha(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pipelineLimitPerProjectUserSha"))

    @pipeline_limit_per_project_user_sha.setter
    def pipeline_limit_per_project_user_sha(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397dbe39991fd386b30e675a8ba7dc1213bf27c52d9f94d0c22bcad6908ea225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineLimitPerProjectUserSha", value)

    @builtins.property
    @jsii.member(jsii_name="plantumlEnabled")
    def plantuml_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "plantumlEnabled"))

    @plantuml_enabled.setter
    def plantuml_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01244d310e63cc77c7f6dacdfc901fd703d91685d588be8bda639db634d1bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plantumlEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="plantumlUrl")
    def plantuml_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "plantumlUrl"))

    @plantuml_url.setter
    def plantuml_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed3afcbf0b1612e2255524a417babf2d3a058331b3961cc87564b1bf67d1279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plantumlUrl", value)

    @builtins.property
    @jsii.member(jsii_name="pollingIntervalMultiplier")
    def polling_interval_multiplier(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pollingIntervalMultiplier"))

    @polling_interval_multiplier.setter
    def polling_interval_multiplier(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c548f2c0808730f9d1c62de700bb9ef294ee4b579e7d30c33cbd8fd520a0581)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pollingIntervalMultiplier", value)

    @builtins.property
    @jsii.member(jsii_name="projectExportEnabled")
    def project_export_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "projectExportEnabled"))

    @project_export_enabled.setter
    def project_export_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b13836813f19f67abfef06f04d62d327bd4249448df02d713a3990c8fd72aa69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectExportEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="prometheusMetricsEnabled")
    def prometheus_metrics_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "prometheusMetricsEnabled"))

    @prometheus_metrics_enabled.setter
    def prometheus_metrics_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0751641429446f7f7669472813a3bea8cfe5cfe53b2491b204bd6bee26834ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prometheusMetricsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="protectedCiVariables")
    def protected_ci_variables(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "protectedCiVariables"))

    @protected_ci_variables.setter
    def protected_ci_variables(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15dcb7261c894ca4361571f53196f7d93489f8026ba918e56f7a6aca99dd08d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protectedCiVariables", value)

    @builtins.property
    @jsii.member(jsii_name="pushEventActivitiesLimit")
    def push_event_activities_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pushEventActivitiesLimit"))

    @push_event_activities_limit.setter
    def push_event_activities_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2615da62324d55a672c129966772980d62a9b5f66fc98ada3a11f53818a001e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushEventActivitiesLimit", value)

    @builtins.property
    @jsii.member(jsii_name="pushEventHooksLimit")
    def push_event_hooks_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pushEventHooksLimit"))

    @push_event_hooks_limit.setter
    def push_event_hooks_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cd1b7b1ffb39eb2f2b3c6e444275c94cbf8b890883af5b83fd5e2c0c42ceacb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushEventHooksLimit", value)

    @builtins.property
    @jsii.member(jsii_name="pypiPackageRequestsForwarding")
    def pypi_package_requests_forwarding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pypiPackageRequestsForwarding"))

    @pypi_package_requests_forwarding.setter
    def pypi_package_requests_forwarding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6bf5a5bf6b2ecb3e8bd3bc7c68fb56528dac9f68c689ab2f2189efdeac3d76e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pypiPackageRequestsForwarding", value)

    @builtins.property
    @jsii.member(jsii_name="rateLimitingResponseText")
    def rate_limiting_response_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rateLimitingResponseText"))

    @rate_limiting_response_text.setter
    def rate_limiting_response_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f3ef6650c38d975c9bcb43ae9ffff8af8131885395f4917a4f4f081a74e917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rateLimitingResponseText", value)

    @builtins.property
    @jsii.member(jsii_name="rawBlobRequestLimit")
    def raw_blob_request_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rawBlobRequestLimit"))

    @raw_blob_request_limit.setter
    def raw_blob_request_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1957233ea41acd5835f1572354ac68b030b8df483b733b36ac61c9c71178839a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawBlobRequestLimit", value)

    @builtins.property
    @jsii.member(jsii_name="recaptchaEnabled")
    def recaptcha_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "recaptchaEnabled"))

    @recaptcha_enabled.setter
    def recaptcha_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102ecb9e503e6226387700430566413e3471bde5dc66cf0a9241af5d3a7c2fe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recaptchaEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="recaptchaPrivateKey")
    def recaptcha_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recaptchaPrivateKey"))

    @recaptcha_private_key.setter
    def recaptcha_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2e6b1146b6a969011e371c7f94fa794adcdbe4137bdaa61330ce9adbd9945ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recaptchaPrivateKey", value)

    @builtins.property
    @jsii.member(jsii_name="recaptchaSiteKey")
    def recaptcha_site_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recaptchaSiteKey"))

    @recaptcha_site_key.setter
    def recaptcha_site_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9c844bae03ec16295641d26c30f99e682bacd7c3e00451a750310b5ec36fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recaptchaSiteKey", value)

    @builtins.property
    @jsii.member(jsii_name="receiveMaxInputSize")
    def receive_max_input_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "receiveMaxInputSize"))

    @receive_max_input_size.setter
    def receive_max_input_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc893e0d8697bb32a6017c3ebee75048b7544721676c58f84c05ec92f106acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "receiveMaxInputSize", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryChecksEnabled")
    def repository_checks_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "repositoryChecksEnabled"))

    @repository_checks_enabled.setter
    def repository_checks_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722ab4d7375476bb665ad8e39ad584aefe8aa712243a3d050bd9ede18e63d6f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryChecksEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="repositorySizeLimit")
    def repository_size_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "repositorySizeLimit"))

    @repository_size_limit.setter
    def repository_size_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cacce962f8ea17c3c9608f484b36ddaef1d21739cb7b703edb9adcf2962a52b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositorySizeLimit", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryStorages")
    def repository_storages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "repositoryStorages"))

    @repository_storages.setter
    def repository_storages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a79f5f10f31808431b8b3c2a8a3764a980d2d19cd069189fa821fcbbc0d6ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryStorages", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryStoragesWeighted")
    def repository_storages_weighted(self) -> typing.Mapping[builtins.str, jsii.Number]:
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "repositoryStoragesWeighted"))

    @repository_storages_weighted.setter
    def repository_storages_weighted(
        self,
        value: typing.Mapping[builtins.str, jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff93a7f9f26ca7253f860d2e7ad9cf0d3b58e8aba63689dd68ba267692108eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryStoragesWeighted", value)

    @builtins.property
    @jsii.member(jsii_name="requireAdminApprovalAfterUserSignup")
    def require_admin_approval_after_user_signup(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireAdminApprovalAfterUserSignup"))

    @require_admin_approval_after_user_signup.setter
    def require_admin_approval_after_user_signup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd213053e802470cbecc9cf0ce5fc7b35e57ad59ddd86fe91f9fbc2485dcf02c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAdminApprovalAfterUserSignup", value)

    @builtins.property
    @jsii.member(jsii_name="requireTwoFactorAuthentication")
    def require_two_factor_authentication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireTwoFactorAuthentication"))

    @require_two_factor_authentication.setter
    def require_two_factor_authentication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79792c861918a68c7aac824e823ca2602d6859da06e7df5b6c83e1e4accc8da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireTwoFactorAuthentication", value)

    @builtins.property
    @jsii.member(jsii_name="restrictedVisibilityLevels")
    def restricted_visibility_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedVisibilityLevels"))

    @restricted_visibility_levels.setter
    def restricted_visibility_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__014984cca0761fbbce824e98cbbb8f6210797a90e5f46374567236617088bf15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restrictedVisibilityLevels", value)

    @builtins.property
    @jsii.member(jsii_name="rsaKeyRestriction")
    def rsa_key_restriction(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rsaKeyRestriction"))

    @rsa_key_restriction.setter
    def rsa_key_restriction(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c4b2fc48459271dc56f752cc5c78f5306b6ab09939eaaea57e7b7dbde5ed7f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaKeyRestriction", value)

    @builtins.property
    @jsii.member(jsii_name="searchRateLimit")
    def search_rate_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "searchRateLimit"))

    @search_rate_limit.setter
    def search_rate_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c169921079c0f1c59af846856152c006e026e89c5f7aae8dfed277b7cd02534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchRateLimit", value)

    @builtins.property
    @jsii.member(jsii_name="searchRateLimitUnauthenticated")
    def search_rate_limit_unauthenticated(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "searchRateLimitUnauthenticated"))

    @search_rate_limit_unauthenticated.setter
    def search_rate_limit_unauthenticated(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06efac3a61ad810ebc4aec4fcac75b711ea8df46a2668beb87cfe60a56581ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchRateLimitUnauthenticated", value)

    @builtins.property
    @jsii.member(jsii_name="sendUserConfirmationEmail")
    def send_user_confirmation_email(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendUserConfirmationEmail"))

    @send_user_confirmation_email.setter
    def send_user_confirmation_email(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67837aa9f2abff375171fbdf1087ec883870dea0960a890a35c92c8088614435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendUserConfirmationEmail", value)

    @builtins.property
    @jsii.member(jsii_name="sessionExpireDelay")
    def session_expire_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionExpireDelay"))

    @session_expire_delay.setter
    def session_expire_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__771a3286fb612560296eb9c2efdd6a8fdf77250aaa15df43858da1f9a842abc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionExpireDelay", value)

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersEnabled")
    def shared_runners_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sharedRunnersEnabled"))

    @shared_runners_enabled.setter
    def shared_runners_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b3116108d005bc6e5880187e50fa9cae3887bf1637dd6dd57494cf83048427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedRunnersEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersMinutes")
    def shared_runners_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sharedRunnersMinutes"))

    @shared_runners_minutes.setter
    def shared_runners_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18ad226c5e99504a3e392445987b6d6d59c6c2888aa165ecbbc5d89a4cdb09a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedRunnersMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="sharedRunnersText")
    def shared_runners_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedRunnersText"))

    @shared_runners_text.setter
    def shared_runners_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5203e60f339316ae4573936bc9aee3c436f4cf9da8412c4f6ab61211bf0e18e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedRunnersText", value)

    @builtins.property
    @jsii.member(jsii_name="sidekiqJobLimiterCompressionThresholdBytes")
    def sidekiq_job_limiter_compression_threshold_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sidekiqJobLimiterCompressionThresholdBytes"))

    @sidekiq_job_limiter_compression_threshold_bytes.setter
    def sidekiq_job_limiter_compression_threshold_bytes(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b0b8099beb4432e50c55fd90deb894ad4305ecf7714ea7a239e700219bc7e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sidekiqJobLimiterCompressionThresholdBytes", value)

    @builtins.property
    @jsii.member(jsii_name="sidekiqJobLimiterLimitBytes")
    def sidekiq_job_limiter_limit_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sidekiqJobLimiterLimitBytes"))

    @sidekiq_job_limiter_limit_bytes.setter
    def sidekiq_job_limiter_limit_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1ca2d9c3d39684eeb3d250cdf1ba7f2fc4c36762699f155800d1d4e09966f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sidekiqJobLimiterLimitBytes", value)

    @builtins.property
    @jsii.member(jsii_name="sidekiqJobLimiterMode")
    def sidekiq_job_limiter_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sidekiqJobLimiterMode"))

    @sidekiq_job_limiter_mode.setter
    def sidekiq_job_limiter_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db959f5ec543832e64571b6b4619b12915a89d9d34b0d7d1247ad74ecdf0c5a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sidekiqJobLimiterMode", value)

    @builtins.property
    @jsii.member(jsii_name="signInText")
    def sign_in_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signInText"))

    @sign_in_text.setter
    def sign_in_text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0c7d6e6e860f60cf83df049d15bcd503ece0fc317960cc8d4712932b634caf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signInText", value)

    @builtins.property
    @jsii.member(jsii_name="signupEnabled")
    def signup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "signupEnabled"))

    @signup_enabled.setter
    def signup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0643bdc5370f67d2fd0ec9035c2c2170a4a4dce7095e547d740f4e653d73e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signupEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="slackAppEnabled")
    def slack_app_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "slackAppEnabled"))

    @slack_app_enabled.setter
    def slack_app_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__774b00ffc67699a5f0aa73fc3b9c4b3051dfedcde18dfa7354486510d7d3cf59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slackAppEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="slackAppId")
    def slack_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slackAppId"))

    @slack_app_id.setter
    def slack_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aafbb6b78303ce93be9a4b2342895cbc6d72064f7ef26700d3770b82ebee4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slackAppId", value)

    @builtins.property
    @jsii.member(jsii_name="slackAppSecret")
    def slack_app_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slackAppSecret"))

    @slack_app_secret.setter
    def slack_app_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0976d4ca51430c2d725e9ef14468ce4f445bb004f2fe8a3709d65f7a6eb3cea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slackAppSecret", value)

    @builtins.property
    @jsii.member(jsii_name="slackAppSigningSecret")
    def slack_app_signing_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slackAppSigningSecret"))

    @slack_app_signing_secret.setter
    def slack_app_signing_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c5d883d2a275d7bc3cc32fff6bd7adadaae3856f9f0e1cdea80948a94fdb323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slackAppSigningSecret", value)

    @builtins.property
    @jsii.member(jsii_name="slackAppVerificationToken")
    def slack_app_verification_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "slackAppVerificationToken"))

    @slack_app_verification_token.setter
    def slack_app_verification_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c217021cb03104cc9e5cf6c833f107032af3d5d563e072de7cff033e40cdef14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slackAppVerificationToken", value)

    @builtins.property
    @jsii.member(jsii_name="snippetSizeLimit")
    def snippet_size_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "snippetSizeLimit"))

    @snippet_size_limit.setter
    def snippet_size_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0105f8e7dde004cfd8d916dc6dcf3d23b8d86103fb773257f41d563c8346d0da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snippetSizeLimit", value)

    @builtins.property
    @jsii.member(jsii_name="snowplowAppId")
    def snowplow_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snowplowAppId"))

    @snowplow_app_id.setter
    def snowplow_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7cc9c17fceac4b950fb7a12eb3a767410aafc8c6582e1d8cd137cd2b60d6561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snowplowAppId", value)

    @builtins.property
    @jsii.member(jsii_name="snowplowCollectorHostname")
    def snowplow_collector_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snowplowCollectorHostname"))

    @snowplow_collector_hostname.setter
    def snowplow_collector_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36503f45aec174140294ae242f02907800a8a50a1842fe136876e0a63a9d8fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snowplowCollectorHostname", value)

    @builtins.property
    @jsii.member(jsii_name="snowplowCookieDomain")
    def snowplow_cookie_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snowplowCookieDomain"))

    @snowplow_cookie_domain.setter
    def snowplow_cookie_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b4cab95c74923759ea4cdd0d3b1550ff57db433a7bbe61da02f7db984d0803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snowplowCookieDomain", value)

    @builtins.property
    @jsii.member(jsii_name="snowplowEnabled")
    def snowplow_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "snowplowEnabled"))

    @snowplow_enabled.setter
    def snowplow_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4529d7caa366c1c495fce7b7f92065f4dce0340b098f0a776e156c848c0f8def)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snowplowEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="sourcegraphEnabled")
    def sourcegraph_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sourcegraphEnabled"))

    @sourcegraph_enabled.setter
    def sourcegraph_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc71d65f9c6a71afad5c454c8b9ab62e4c2edef76aecbb3d83acce365389b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcegraphEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="sourcegraphPublicOnly")
    def sourcegraph_public_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sourcegraphPublicOnly"))

    @sourcegraph_public_only.setter
    def sourcegraph_public_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821e13884cb3f294d531fceb12e8bf261bb3b16226e74d725b24e71f7ebfd231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcegraphPublicOnly", value)

    @builtins.property
    @jsii.member(jsii_name="sourcegraphUrl")
    def sourcegraph_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourcegraphUrl"))

    @sourcegraph_url.setter
    def sourcegraph_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2dd3fe47585e5638ab00f2dab5c2f89165f7b9aa8959a77e88cbfe77191101d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourcegraphUrl", value)

    @builtins.property
    @jsii.member(jsii_name="spamCheckApiKey")
    def spam_check_api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spamCheckApiKey"))

    @spam_check_api_key.setter
    def spam_check_api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809b9ada1e16fab6e8130aa10c8d2d42e708ff5ac43df6ffde8e67ebe33d05bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spamCheckApiKey", value)

    @builtins.property
    @jsii.member(jsii_name="spamCheckEndpointEnabled")
    def spam_check_endpoint_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "spamCheckEndpointEnabled"))

    @spam_check_endpoint_enabled.setter
    def spam_check_endpoint_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db02870aa00bc04b0202077056377d300634891740064930d0dc8f51fd1d2bf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spamCheckEndpointEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="spamCheckEndpointUrl")
    def spam_check_endpoint_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spamCheckEndpointUrl"))

    @spam_check_endpoint_url.setter
    def spam_check_endpoint_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4a7d16b71eccf9d9d03851fbeaf650163337c5047a8bbe061766ad19442147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spamCheckEndpointUrl", value)

    @builtins.property
    @jsii.member(jsii_name="suggestPipelineEnabled")
    def suggest_pipeline_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suggestPipelineEnabled"))

    @suggest_pipeline_enabled.setter
    def suggest_pipeline_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4040207b681d5aadf6f3a9ad41a57cb84d4c33591cb391d53591b884a6d5e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suggestPipelineEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="terminalMaxSessionTime")
    def terminal_max_session_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminalMaxSessionTime"))

    @terminal_max_session_time.setter
    def terminal_max_session_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a099e532cafade9f1107acab326529d50151dba85cc0892cf32634b3ec0717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminalMaxSessionTime", value)

    @builtins.property
    @jsii.member(jsii_name="terms")
    def terms(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terms"))

    @terms.setter
    def terms(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc49516b8fe9e35a916659f708ef0c19cc68dbc36d00391f2d0f9c9596dda709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terms", value)

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedApiEnabled")
    def throttle_authenticated_api_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "throttleAuthenticatedApiEnabled"))

    @throttle_authenticated_api_enabled.setter
    def throttle_authenticated_api_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b7f170397d65a92ca24a6a5d14adc2956da08161bce7d7f655808e5b9899f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleAuthenticatedApiEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedApiPeriodInSeconds")
    def throttle_authenticated_api_period_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleAuthenticatedApiPeriodInSeconds"))

    @throttle_authenticated_api_period_in_seconds.setter
    def throttle_authenticated_api_period_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a99dc518c5bc8a646f005b95a2250d72b88ae61c2387d0c075925209be5ca1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleAuthenticatedApiPeriodInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedApiRequestsPerPeriod")
    def throttle_authenticated_api_requests_per_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleAuthenticatedApiRequestsPerPeriod"))

    @throttle_authenticated_api_requests_per_period.setter
    def throttle_authenticated_api_requests_per_period(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98003193344171b455bd8dca3e3bfd8aa76a536914de3c94274081ea200e63fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleAuthenticatedApiRequestsPerPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedPackagesApiEnabled")
    def throttle_authenticated_packages_api_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "throttleAuthenticatedPackagesApiEnabled"))

    @throttle_authenticated_packages_api_enabled.setter
    def throttle_authenticated_packages_api_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363bd5d55745915c8ad758f8f23c449d0db75eb3d008d813dd3354455eac288f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleAuthenticatedPackagesApiEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedPackagesApiPeriodInSeconds")
    def throttle_authenticated_packages_api_period_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleAuthenticatedPackagesApiPeriodInSeconds"))

    @throttle_authenticated_packages_api_period_in_seconds.setter
    def throttle_authenticated_packages_api_period_in_seconds(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4141e09107fc67128670f0f4caaf75a71f76100eb77dd6fafb4a98e583c39d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleAuthenticatedPackagesApiPeriodInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedPackagesApiRequestsPerPeriod")
    def throttle_authenticated_packages_api_requests_per_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleAuthenticatedPackagesApiRequestsPerPeriod"))

    @throttle_authenticated_packages_api_requests_per_period.setter
    def throttle_authenticated_packages_api_requests_per_period(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb41bdd1b3c2fead2e4556e32f000447efcf37c89cee503648639a509ae0266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleAuthenticatedPackagesApiRequestsPerPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedWebEnabled")
    def throttle_authenticated_web_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "throttleAuthenticatedWebEnabled"))

    @throttle_authenticated_web_enabled.setter
    def throttle_authenticated_web_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d82949e4417f718fe69516c47a4be60ffeab7f12016ef3562a824a559c2f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleAuthenticatedWebEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedWebPeriodInSeconds")
    def throttle_authenticated_web_period_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleAuthenticatedWebPeriodInSeconds"))

    @throttle_authenticated_web_period_in_seconds.setter
    def throttle_authenticated_web_period_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65128c503945a5bc2c599f1d4cbc81113e3aa6b1f6f656bdb20495f04c7ae29a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleAuthenticatedWebPeriodInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="throttleAuthenticatedWebRequestsPerPeriod")
    def throttle_authenticated_web_requests_per_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleAuthenticatedWebRequestsPerPeriod"))

    @throttle_authenticated_web_requests_per_period.setter
    def throttle_authenticated_web_requests_per_period(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c727224210e2010a9829f9876009406b87c758cda74545dfaa727f42299588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleAuthenticatedWebRequestsPerPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedApiEnabled")
    def throttle_unauthenticated_api_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "throttleUnauthenticatedApiEnabled"))

    @throttle_unauthenticated_api_enabled.setter
    def throttle_unauthenticated_api_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63935ce53157de1993e608c3ab25b06f0df5269839cc1753e9c421b90b4459e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleUnauthenticatedApiEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedApiPeriodInSeconds")
    def throttle_unauthenticated_api_period_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleUnauthenticatedApiPeriodInSeconds"))

    @throttle_unauthenticated_api_period_in_seconds.setter
    def throttle_unauthenticated_api_period_in_seconds(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a636881d648ce07d1875163a672d3a3d52c1588087acb699f89a2b5ba85e23e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleUnauthenticatedApiPeriodInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedApiRequestsPerPeriod")
    def throttle_unauthenticated_api_requests_per_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleUnauthenticatedApiRequestsPerPeriod"))

    @throttle_unauthenticated_api_requests_per_period.setter
    def throttle_unauthenticated_api_requests_per_period(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2013017adcaf76b68d9e8b4e0b90e96e84071b4abf4eb152c07288c833f93791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleUnauthenticatedApiRequestsPerPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedPackagesApiEnabled")
    def throttle_unauthenticated_packages_api_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "throttleUnauthenticatedPackagesApiEnabled"))

    @throttle_unauthenticated_packages_api_enabled.setter
    def throttle_unauthenticated_packages_api_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881bd1528d14845f681f6d27e071252c72f9cd9ec4337ba63ea97e9e223cbef9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleUnauthenticatedPackagesApiEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedPackagesApiPeriodInSeconds")
    def throttle_unauthenticated_packages_api_period_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleUnauthenticatedPackagesApiPeriodInSeconds"))

    @throttle_unauthenticated_packages_api_period_in_seconds.setter
    def throttle_unauthenticated_packages_api_period_in_seconds(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ac867a5a84551164b17dbf2723ec471496fdf01fe3622011ae485a7d8ff3e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleUnauthenticatedPackagesApiPeriodInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedPackagesApiRequestsPerPeriod")
    def throttle_unauthenticated_packages_api_requests_per_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleUnauthenticatedPackagesApiRequestsPerPeriod"))

    @throttle_unauthenticated_packages_api_requests_per_period.setter
    def throttle_unauthenticated_packages_api_requests_per_period(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae50d1553a6acceb9b0cb3ce7a649dc8a7539ec3c0205b120ebefb399e33fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleUnauthenticatedPackagesApiRequestsPerPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedWebEnabled")
    def throttle_unauthenticated_web_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "throttleUnauthenticatedWebEnabled"))

    @throttle_unauthenticated_web_enabled.setter
    def throttle_unauthenticated_web_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__948de55c1e4c2b951947365d1cd59dc7d9eab1249f65b20e398414df0982f1bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleUnauthenticatedWebEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedWebPeriodInSeconds")
    def throttle_unauthenticated_web_period_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleUnauthenticatedWebPeriodInSeconds"))

    @throttle_unauthenticated_web_period_in_seconds.setter
    def throttle_unauthenticated_web_period_in_seconds(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4978b08f915757d709ad4ef7b9bc73fc425419c94f001606c6fdb2af4b95e513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleUnauthenticatedWebPeriodInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="throttleUnauthenticatedWebRequestsPerPeriod")
    def throttle_unauthenticated_web_requests_per_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttleUnauthenticatedWebRequestsPerPeriod"))

    @throttle_unauthenticated_web_requests_per_period.setter
    def throttle_unauthenticated_web_requests_per_period(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e636a9a0b817a43fa0f39c2469e57eeb627716e0031fa640bd4b65a5c3c607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttleUnauthenticatedWebRequestsPerPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="timeTrackingLimitToHours")
    def time_tracking_limit_to_hours(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "timeTrackingLimitToHours"))

    @time_tracking_limit_to_hours.setter
    def time_tracking_limit_to_hours(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6203d46a2aff03f6781334a47a98c5f345e8cd4e4ff1b9023a789988750e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeTrackingLimitToHours", value)

    @builtins.property
    @jsii.member(jsii_name="twoFactorGracePeriod")
    def two_factor_grace_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "twoFactorGracePeriod"))

    @two_factor_grace_period.setter
    def two_factor_grace_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2889d24f1c18a31ded8d26772d11c7d2070629cef13072a357bfe0d0d7210dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twoFactorGracePeriod", value)

    @builtins.property
    @jsii.member(jsii_name="uniqueIpsLimitEnabled")
    def unique_ips_limit_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "uniqueIpsLimitEnabled"))

    @unique_ips_limit_enabled.setter
    def unique_ips_limit_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810b9dda6f58abf0039a94974810b81e552631a1bdd36e3ca5525b75c1276b5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniqueIpsLimitEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="uniqueIpsLimitPerUser")
    def unique_ips_limit_per_user(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "uniqueIpsLimitPerUser"))

    @unique_ips_limit_per_user.setter
    def unique_ips_limit_per_user(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe0650128f4cf780f0a2915b1e32445ee8696b19ea0fa7f9b51657723d7afcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniqueIpsLimitPerUser", value)

    @builtins.property
    @jsii.member(jsii_name="uniqueIpsLimitTimeWindow")
    def unique_ips_limit_time_window(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "uniqueIpsLimitTimeWindow"))

    @unique_ips_limit_time_window.setter
    def unique_ips_limit_time_window(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0c4554cc41b227b1cd23ede4f55271c0e38435759587e6f9f7dce381b39228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniqueIpsLimitTimeWindow", value)

    @builtins.property
    @jsii.member(jsii_name="usagePingEnabled")
    def usage_ping_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "usagePingEnabled"))

    @usage_ping_enabled.setter
    def usage_ping_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248d53078b8907c6120b1a0e8fc1c128b74d48f5d13a6f3aa0d06df7272cec7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usagePingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="userDeactivationEmailsEnabled")
    def user_deactivation_emails_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "userDeactivationEmailsEnabled"))

    @user_deactivation_emails_enabled.setter
    def user_deactivation_emails_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5526514a99981349d177fa6f57768f803c82234f9c1eea2a6eabc05521f3fae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDeactivationEmailsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="userDefaultExternal")
    def user_default_external(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "userDefaultExternal"))

    @user_default_external.setter
    def user_default_external(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd7206d25baff569e6348a26a5c0fc760ce42a20f47e354e018af57f0552981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDefaultExternal", value)

    @builtins.property
    @jsii.member(jsii_name="userDefaultInternalRegex")
    def user_default_internal_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userDefaultInternalRegex"))

    @user_default_internal_regex.setter
    def user_default_internal_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7d15f089aa9d346a6458f91e2fbc568da255334df9f1d83c9b80f973d17c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDefaultInternalRegex", value)

    @builtins.property
    @jsii.member(jsii_name="userOauthApplications")
    def user_oauth_applications(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "userOauthApplications"))

    @user_oauth_applications.setter
    def user_oauth_applications(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7668c25cdb8cd238202f05d6917384eea1f38391fcae1c6c400803854c3b165f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userOauthApplications", value)

    @builtins.property
    @jsii.member(jsii_name="userShowAddSshKeyMessage")
    def user_show_add_ssh_key_message(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "userShowAddSshKeyMessage"))

    @user_show_add_ssh_key_message.setter
    def user_show_add_ssh_key_message(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ffdcecbaa9bb071ba18049e109dbd21b1ea75a25bb530afb7f4e38e5b37454c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userShowAddSshKeyMessage", value)

    @builtins.property
    @jsii.member(jsii_name="versionCheckEnabled")
    def version_check_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "versionCheckEnabled"))

    @version_check_enabled.setter
    def version_check_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c26da11252c881468bd451a23577f6762ffd24c5e6344c7dc9e3569649532ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionCheckEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="webIdeClientsidePreviewEnabled")
    def web_ide_clientside_preview_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "webIdeClientsidePreviewEnabled"))

    @web_ide_clientside_preview_enabled.setter
    def web_ide_clientside_preview_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a28320ae7a9b4b14eb48b6bd7175269fd6cc51ad33df62db9ac38717d53636d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webIdeClientsidePreviewEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="whatsNewVariant")
    def whats_new_variant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "whatsNewVariant"))

    @whats_new_variant.setter
    def whats_new_variant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03a40b699ab248d4fc8ba417d6c1d7e350c29cb494a4c594cfd6cd401e36dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "whatsNewVariant", value)

    @builtins.property
    @jsii.member(jsii_name="wikiPageMaxContentBytes")
    def wiki_page_max_content_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "wikiPageMaxContentBytes"))

    @wiki_page_max_content_bytes.setter
    def wiki_page_max_content_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7f961fa567c203b84eb5b0fbfa3e065a5025582305a3b108bfa2fa7f002f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wikiPageMaxContentBytes", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-gitlab.applicationSettings.ApplicationSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "abuse_notification_email": "abuseNotificationEmail",
        "admin_mode": "adminMode",
        "after_sign_out_path": "afterSignOutPath",
        "after_sign_up_text": "afterSignUpText",
        "akismet_api_key": "akismetApiKey",
        "akismet_enabled": "akismetEnabled",
        "allow_group_owners_to_manage_ldap": "allowGroupOwnersToManageLdap",
        "allow_local_requests_from_system_hooks": "allowLocalRequestsFromSystemHooks",
        "allow_local_requests_from_web_hooks_and_services": "allowLocalRequestsFromWebHooksAndServices",
        "archive_builds_in_human_readable": "archiveBuildsInHumanReadable",
        "asset_proxy_allowlist": "assetProxyAllowlist",
        "asset_proxy_enabled": "assetProxyEnabled",
        "asset_proxy_secret_key": "assetProxySecretKey",
        "asset_proxy_url": "assetProxyUrl",
        "authorized_keys_enabled": "authorizedKeysEnabled",
        "auto_devops_domain": "autoDevopsDomain",
        "auto_devops_enabled": "autoDevopsEnabled",
        "automatic_purchased_storage_allocation": "automaticPurchasedStorageAllocation",
        "can_create_group": "canCreateGroup",
        "check_namespace_plan": "checkNamespacePlan",
        "commit_email_hostname": "commitEmailHostname",
        "container_expiration_policies_enable_historic_entries": "containerExpirationPoliciesEnableHistoricEntries",
        "container_registry_cleanup_tags_service_max_list_size": "containerRegistryCleanupTagsServiceMaxListSize",
        "container_registry_delete_tags_service_timeout": "containerRegistryDeleteTagsServiceTimeout",
        "container_registry_expiration_policies_caching": "containerRegistryExpirationPoliciesCaching",
        "container_registry_expiration_policies_worker_capacity": "containerRegistryExpirationPoliciesWorkerCapacity",
        "container_registry_token_expire_delay": "containerRegistryTokenExpireDelay",
        "deactivate_dormant_users": "deactivateDormantUsers",
        "default_artifacts_expire_in": "defaultArtifactsExpireIn",
        "default_branch_name": "defaultBranchName",
        "default_branch_protection": "defaultBranchProtection",
        "default_ci_config_path": "defaultCiConfigPath",
        "default_group_visibility": "defaultGroupVisibility",
        "default_project_creation": "defaultProjectCreation",
        "default_projects_limit": "defaultProjectsLimit",
        "default_project_visibility": "defaultProjectVisibility",
        "default_snippet_visibility": "defaultSnippetVisibility",
        "delayed_group_deletion": "delayedGroupDeletion",
        "delayed_project_deletion": "delayedProjectDeletion",
        "delete_inactive_projects": "deleteInactiveProjects",
        "deletion_adjourned_period": "deletionAdjournedPeriod",
        "diff_max_files": "diffMaxFiles",
        "diff_max_lines": "diffMaxLines",
        "diff_max_patch_bytes": "diffMaxPatchBytes",
        "disabled_oauth_sign_in_sources": "disabledOauthSignInSources",
        "disable_feed_token": "disableFeedToken",
        "dns_rebinding_protection_enabled": "dnsRebindingProtectionEnabled",
        "domain_allowlist": "domainAllowlist",
        "domain_denylist": "domainDenylist",
        "domain_denylist_enabled": "domainDenylistEnabled",
        "dsa_key_restriction": "dsaKeyRestriction",
        "ecdsa_key_restriction": "ecdsaKeyRestriction",
        "ecdsa_sk_key_restriction": "ecdsaSkKeyRestriction",
        "ed25519_key_restriction": "ed25519KeyRestriction",
        "ed25519_sk_key_restriction": "ed25519SkKeyRestriction",
        "eks_access_key_id": "eksAccessKeyId",
        "eks_account_id": "eksAccountId",
        "eks_integration_enabled": "eksIntegrationEnabled",
        "eks_secret_access_key": "eksSecretAccessKey",
        "elasticsearch_aws": "elasticsearchAws",
        "elasticsearch_aws_access_key": "elasticsearchAwsAccessKey",
        "elasticsearch_aws_region": "elasticsearchAwsRegion",
        "elasticsearch_aws_secret_access_key": "elasticsearchAwsSecretAccessKey",
        "elasticsearch_indexed_field_length_limit": "elasticsearchIndexedFieldLengthLimit",
        "elasticsearch_indexed_file_size_limit_kb": "elasticsearchIndexedFileSizeLimitKb",
        "elasticsearch_indexing": "elasticsearchIndexing",
        "elasticsearch_limit_indexing": "elasticsearchLimitIndexing",
        "elasticsearch_max_bulk_concurrency": "elasticsearchMaxBulkConcurrency",
        "elasticsearch_max_bulk_size_mb": "elasticsearchMaxBulkSizeMb",
        "elasticsearch_namespace_ids": "elasticsearchNamespaceIds",
        "elasticsearch_password": "elasticsearchPassword",
        "elasticsearch_project_ids": "elasticsearchProjectIds",
        "elasticsearch_search": "elasticsearchSearch",
        "elasticsearch_url": "elasticsearchUrl",
        "elasticsearch_username": "elasticsearchUsername",
        "email_additional_text": "emailAdditionalText",
        "email_author_in_body": "emailAuthorInBody",
        "enabled_git_access_protocol": "enabledGitAccessProtocol",
        "enforce_namespace_storage_limit": "enforceNamespaceStorageLimit",
        "enforce_terms": "enforceTerms",
        "external_auth_client_cert": "externalAuthClientCert",
        "external_auth_client_key": "externalAuthClientKey",
        "external_auth_client_key_pass": "externalAuthClientKeyPass",
        "external_authorization_service_default_label": "externalAuthorizationServiceDefaultLabel",
        "external_authorization_service_enabled": "externalAuthorizationServiceEnabled",
        "external_authorization_service_timeout": "externalAuthorizationServiceTimeout",
        "external_authorization_service_url": "externalAuthorizationServiceUrl",
        "external_pipeline_validation_service_timeout": "externalPipelineValidationServiceTimeout",
        "external_pipeline_validation_service_token": "externalPipelineValidationServiceToken",
        "external_pipeline_validation_service_url": "externalPipelineValidationServiceUrl",
        "file_template_project_id": "fileTemplateProjectId",
        "first_day_of_week": "firstDayOfWeek",
        "geo_node_allowed_ips": "geoNodeAllowedIps",
        "geo_status_timeout": "geoStatusTimeout",
        "gitaly_timeout_default": "gitalyTimeoutDefault",
        "gitaly_timeout_fast": "gitalyTimeoutFast",
        "gitaly_timeout_medium": "gitalyTimeoutMedium",
        "git_rate_limit_users_allowlist": "gitRateLimitUsersAllowlist",
        "git_two_factor_session_expiry": "gitTwoFactorSessionExpiry",
        "grafana_enabled": "grafanaEnabled",
        "grafana_url": "grafanaUrl",
        "gravatar_enabled": "gravatarEnabled",
        "group_owners_can_manage_default_branch_protection": "groupOwnersCanManageDefaultBranchProtection",
        "hashed_storage_enabled": "hashedStorageEnabled",
        "help_page_hide_commercial_content": "helpPageHideCommercialContent",
        "help_page_support_url": "helpPageSupportUrl",
        "help_page_text": "helpPageText",
        "help_text": "helpText",
        "hide_third_party_offers": "hideThirdPartyOffers",
        "home_page_url": "homePageUrl",
        "housekeeping_enabled": "housekeepingEnabled",
        "housekeeping_full_repack_period": "housekeepingFullRepackPeriod",
        "housekeeping_gc_period": "housekeepingGcPeriod",
        "housekeeping_incremental_repack_period": "housekeepingIncrementalRepackPeriod",
        "html_emails_enabled": "htmlEmailsEnabled",
        "id": "id",
        "import_sources": "importSources",
        "inactive_projects_delete_after_months": "inactiveProjectsDeleteAfterMonths",
        "inactive_projects_min_size_mb": "inactiveProjectsMinSizeMb",
        "inactive_projects_send_warning_email_after_months": "inactiveProjectsSendWarningEmailAfterMonths",
        "in_product_marketing_emails_enabled": "inProductMarketingEmailsEnabled",
        "invisible_captcha_enabled": "invisibleCaptchaEnabled",
        "issues_create_limit": "issuesCreateLimit",
        "keep_latest_artifact": "keepLatestArtifact",
        "local_markdown_version": "localMarkdownVersion",
        "mailgun_events_enabled": "mailgunEventsEnabled",
        "mailgun_signing_key": "mailgunSigningKey",
        "maintenance_mode": "maintenanceMode",
        "maintenance_mode_message": "maintenanceModeMessage",
        "max_artifacts_size": "maxArtifactsSize",
        "max_attachment_size": "maxAttachmentSize",
        "max_export_size": "maxExportSize",
        "max_import_size": "maxImportSize",
        "max_number_of_repository_downloads": "maxNumberOfRepositoryDownloads",
        "max_number_of_repository_downloads_within_time_period": "maxNumberOfRepositoryDownloadsWithinTimePeriod",
        "max_pages_size": "maxPagesSize",
        "max_personal_access_token_lifetime": "maxPersonalAccessTokenLifetime",
        "max_ssh_key_lifetime": "maxSshKeyLifetime",
        "metrics_method_call_threshold": "metricsMethodCallThreshold",
        "mirror_available": "mirrorAvailable",
        "mirror_capacity_threshold": "mirrorCapacityThreshold",
        "mirror_max_capacity": "mirrorMaxCapacity",
        "mirror_max_delay": "mirrorMaxDelay",
        "npm_package_requests_forwarding": "npmPackageRequestsForwarding",
        "outbound_local_requests_whitelist": "outboundLocalRequestsWhitelist",
        "package_registry_cleanup_policies_worker_capacity": "packageRegistryCleanupPoliciesWorkerCapacity",
        "pages_domain_verification_enabled": "pagesDomainVerificationEnabled",
        "password_authentication_enabled_for_git": "passwordAuthenticationEnabledForGit",
        "password_authentication_enabled_for_web": "passwordAuthenticationEnabledForWeb",
        "password_lowercase_required": "passwordLowercaseRequired",
        "password_number_required": "passwordNumberRequired",
        "password_symbol_required": "passwordSymbolRequired",
        "password_uppercase_required": "passwordUppercaseRequired",
        "performance_bar_allowed_group_path": "performanceBarAllowedGroupPath",
        "personal_access_token_prefix": "personalAccessTokenPrefix",
        "pipeline_limit_per_project_user_sha": "pipelineLimitPerProjectUserSha",
        "plantuml_enabled": "plantumlEnabled",
        "plantuml_url": "plantumlUrl",
        "polling_interval_multiplier": "pollingIntervalMultiplier",
        "project_export_enabled": "projectExportEnabled",
        "prometheus_metrics_enabled": "prometheusMetricsEnabled",
        "protected_ci_variables": "protectedCiVariables",
        "push_event_activities_limit": "pushEventActivitiesLimit",
        "push_event_hooks_limit": "pushEventHooksLimit",
        "pypi_package_requests_forwarding": "pypiPackageRequestsForwarding",
        "rate_limiting_response_text": "rateLimitingResponseText",
        "raw_blob_request_limit": "rawBlobRequestLimit",
        "recaptcha_enabled": "recaptchaEnabled",
        "recaptcha_private_key": "recaptchaPrivateKey",
        "recaptcha_site_key": "recaptchaSiteKey",
        "receive_max_input_size": "receiveMaxInputSize",
        "repository_checks_enabled": "repositoryChecksEnabled",
        "repository_size_limit": "repositorySizeLimit",
        "repository_storages": "repositoryStorages",
        "repository_storages_weighted": "repositoryStoragesWeighted",
        "require_admin_approval_after_user_signup": "requireAdminApprovalAfterUserSignup",
        "require_two_factor_authentication": "requireTwoFactorAuthentication",
        "restricted_visibility_levels": "restrictedVisibilityLevels",
        "rsa_key_restriction": "rsaKeyRestriction",
        "search_rate_limit": "searchRateLimit",
        "search_rate_limit_unauthenticated": "searchRateLimitUnauthenticated",
        "send_user_confirmation_email": "sendUserConfirmationEmail",
        "session_expire_delay": "sessionExpireDelay",
        "shared_runners_enabled": "sharedRunnersEnabled",
        "shared_runners_minutes": "sharedRunnersMinutes",
        "shared_runners_text": "sharedRunnersText",
        "sidekiq_job_limiter_compression_threshold_bytes": "sidekiqJobLimiterCompressionThresholdBytes",
        "sidekiq_job_limiter_limit_bytes": "sidekiqJobLimiterLimitBytes",
        "sidekiq_job_limiter_mode": "sidekiqJobLimiterMode",
        "sign_in_text": "signInText",
        "signup_enabled": "signupEnabled",
        "slack_app_enabled": "slackAppEnabled",
        "slack_app_id": "slackAppId",
        "slack_app_secret": "slackAppSecret",
        "slack_app_signing_secret": "slackAppSigningSecret",
        "slack_app_verification_token": "slackAppVerificationToken",
        "snippet_size_limit": "snippetSizeLimit",
        "snowplow_app_id": "snowplowAppId",
        "snowplow_collector_hostname": "snowplowCollectorHostname",
        "snowplow_cookie_domain": "snowplowCookieDomain",
        "snowplow_enabled": "snowplowEnabled",
        "sourcegraph_enabled": "sourcegraphEnabled",
        "sourcegraph_public_only": "sourcegraphPublicOnly",
        "sourcegraph_url": "sourcegraphUrl",
        "spam_check_api_key": "spamCheckApiKey",
        "spam_check_endpoint_enabled": "spamCheckEndpointEnabled",
        "spam_check_endpoint_url": "spamCheckEndpointUrl",
        "suggest_pipeline_enabled": "suggestPipelineEnabled",
        "terminal_max_session_time": "terminalMaxSessionTime",
        "terms": "terms",
        "throttle_authenticated_api_enabled": "throttleAuthenticatedApiEnabled",
        "throttle_authenticated_api_period_in_seconds": "throttleAuthenticatedApiPeriodInSeconds",
        "throttle_authenticated_api_requests_per_period": "throttleAuthenticatedApiRequestsPerPeriod",
        "throttle_authenticated_packages_api_enabled": "throttleAuthenticatedPackagesApiEnabled",
        "throttle_authenticated_packages_api_period_in_seconds": "throttleAuthenticatedPackagesApiPeriodInSeconds",
        "throttle_authenticated_packages_api_requests_per_period": "throttleAuthenticatedPackagesApiRequestsPerPeriod",
        "throttle_authenticated_web_enabled": "throttleAuthenticatedWebEnabled",
        "throttle_authenticated_web_period_in_seconds": "throttleAuthenticatedWebPeriodInSeconds",
        "throttle_authenticated_web_requests_per_period": "throttleAuthenticatedWebRequestsPerPeriod",
        "throttle_unauthenticated_api_enabled": "throttleUnauthenticatedApiEnabled",
        "throttle_unauthenticated_api_period_in_seconds": "throttleUnauthenticatedApiPeriodInSeconds",
        "throttle_unauthenticated_api_requests_per_period": "throttleUnauthenticatedApiRequestsPerPeriod",
        "throttle_unauthenticated_packages_api_enabled": "throttleUnauthenticatedPackagesApiEnabled",
        "throttle_unauthenticated_packages_api_period_in_seconds": "throttleUnauthenticatedPackagesApiPeriodInSeconds",
        "throttle_unauthenticated_packages_api_requests_per_period": "throttleUnauthenticatedPackagesApiRequestsPerPeriod",
        "throttle_unauthenticated_web_enabled": "throttleUnauthenticatedWebEnabled",
        "throttle_unauthenticated_web_period_in_seconds": "throttleUnauthenticatedWebPeriodInSeconds",
        "throttle_unauthenticated_web_requests_per_period": "throttleUnauthenticatedWebRequestsPerPeriod",
        "time_tracking_limit_to_hours": "timeTrackingLimitToHours",
        "two_factor_grace_period": "twoFactorGracePeriod",
        "unique_ips_limit_enabled": "uniqueIpsLimitEnabled",
        "unique_ips_limit_per_user": "uniqueIpsLimitPerUser",
        "unique_ips_limit_time_window": "uniqueIpsLimitTimeWindow",
        "usage_ping_enabled": "usagePingEnabled",
        "user_deactivation_emails_enabled": "userDeactivationEmailsEnabled",
        "user_default_external": "userDefaultExternal",
        "user_default_internal_regex": "userDefaultInternalRegex",
        "user_oauth_applications": "userOauthApplications",
        "user_show_add_ssh_key_message": "userShowAddSshKeyMessage",
        "version_check_enabled": "versionCheckEnabled",
        "web_ide_clientside_preview_enabled": "webIdeClientsidePreviewEnabled",
        "whats_new_variant": "whatsNewVariant",
        "wiki_page_max_content_bytes": "wikiPageMaxContentBytes",
    },
)
class ApplicationSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        abuse_notification_email: typing.Optional[builtins.str] = None,
        admin_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        after_sign_out_path: typing.Optional[builtins.str] = None,
        after_sign_up_text: typing.Optional[builtins.str] = None,
        akismet_api_key: typing.Optional[builtins.str] = None,
        akismet_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_group_owners_to_manage_ldap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_local_requests_from_system_hooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_local_requests_from_web_hooks_and_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        archive_builds_in_human_readable: typing.Optional[builtins.str] = None,
        asset_proxy_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
        asset_proxy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        asset_proxy_secret_key: typing.Optional[builtins.str] = None,
        asset_proxy_url: typing.Optional[builtins.str] = None,
        authorized_keys_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_devops_domain: typing.Optional[builtins.str] = None,
        auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        automatic_purchased_storage_allocation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        can_create_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        check_namespace_plan: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        commit_email_hostname: typing.Optional[builtins.str] = None,
        container_expiration_policies_enable_historic_entries: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        container_registry_cleanup_tags_service_max_list_size: typing.Optional[jsii.Number] = None,
        container_registry_delete_tags_service_timeout: typing.Optional[jsii.Number] = None,
        container_registry_expiration_policies_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        container_registry_expiration_policies_worker_capacity: typing.Optional[jsii.Number] = None,
        container_registry_token_expire_delay: typing.Optional[jsii.Number] = None,
        deactivate_dormant_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_artifacts_expire_in: typing.Optional[builtins.str] = None,
        default_branch_name: typing.Optional[builtins.str] = None,
        default_branch_protection: typing.Optional[jsii.Number] = None,
        default_ci_config_path: typing.Optional[builtins.str] = None,
        default_group_visibility: typing.Optional[builtins.str] = None,
        default_project_creation: typing.Optional[jsii.Number] = None,
        default_projects_limit: typing.Optional[jsii.Number] = None,
        default_project_visibility: typing.Optional[builtins.str] = None,
        default_snippet_visibility: typing.Optional[builtins.str] = None,
        delayed_group_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delayed_project_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_inactive_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion_adjourned_period: typing.Optional[jsii.Number] = None,
        diff_max_files: typing.Optional[jsii.Number] = None,
        diff_max_lines: typing.Optional[jsii.Number] = None,
        diff_max_patch_bytes: typing.Optional[jsii.Number] = None,
        disabled_oauth_sign_in_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        disable_feed_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dns_rebinding_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        domain_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_denylist: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_denylist_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dsa_key_restriction: typing.Optional[jsii.Number] = None,
        ecdsa_key_restriction: typing.Optional[jsii.Number] = None,
        ecdsa_sk_key_restriction: typing.Optional[jsii.Number] = None,
        ed25519_key_restriction: typing.Optional[jsii.Number] = None,
        ed25519_sk_key_restriction: typing.Optional[jsii.Number] = None,
        eks_access_key_id: typing.Optional[builtins.str] = None,
        eks_account_id: typing.Optional[builtins.str] = None,
        eks_integration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        eks_secret_access_key: typing.Optional[builtins.str] = None,
        elasticsearch_aws: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        elasticsearch_aws_access_key: typing.Optional[builtins.str] = None,
        elasticsearch_aws_region: typing.Optional[builtins.str] = None,
        elasticsearch_aws_secret_access_key: typing.Optional[builtins.str] = None,
        elasticsearch_indexed_field_length_limit: typing.Optional[jsii.Number] = None,
        elasticsearch_indexed_file_size_limit_kb: typing.Optional[jsii.Number] = None,
        elasticsearch_indexing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        elasticsearch_limit_indexing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        elasticsearch_max_bulk_concurrency: typing.Optional[jsii.Number] = None,
        elasticsearch_max_bulk_size_mb: typing.Optional[jsii.Number] = None,
        elasticsearch_namespace_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        elasticsearch_password: typing.Optional[builtins.str] = None,
        elasticsearch_project_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        elasticsearch_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        elasticsearch_url: typing.Optional[typing.Sequence[builtins.str]] = None,
        elasticsearch_username: typing.Optional[builtins.str] = None,
        email_additional_text: typing.Optional[builtins.str] = None,
        email_author_in_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enabled_git_access_protocol: typing.Optional[builtins.str] = None,
        enforce_namespace_storage_limit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce_terms: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_auth_client_cert: typing.Optional[builtins.str] = None,
        external_auth_client_key: typing.Optional[builtins.str] = None,
        external_auth_client_key_pass: typing.Optional[builtins.str] = None,
        external_authorization_service_default_label: typing.Optional[builtins.str] = None,
        external_authorization_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_authorization_service_timeout: typing.Optional[jsii.Number] = None,
        external_authorization_service_url: typing.Optional[builtins.str] = None,
        external_pipeline_validation_service_timeout: typing.Optional[jsii.Number] = None,
        external_pipeline_validation_service_token: typing.Optional[builtins.str] = None,
        external_pipeline_validation_service_url: typing.Optional[builtins.str] = None,
        file_template_project_id: typing.Optional[jsii.Number] = None,
        first_day_of_week: typing.Optional[jsii.Number] = None,
        geo_node_allowed_ips: typing.Optional[builtins.str] = None,
        geo_status_timeout: typing.Optional[jsii.Number] = None,
        gitaly_timeout_default: typing.Optional[jsii.Number] = None,
        gitaly_timeout_fast: typing.Optional[jsii.Number] = None,
        gitaly_timeout_medium: typing.Optional[jsii.Number] = None,
        git_rate_limit_users_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
        git_two_factor_session_expiry: typing.Optional[jsii.Number] = None,
        grafana_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        grafana_url: typing.Optional[builtins.str] = None,
        gravatar_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        group_owners_can_manage_default_branch_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hashed_storage_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        help_page_hide_commercial_content: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        help_page_support_url: typing.Optional[builtins.str] = None,
        help_page_text: typing.Optional[builtins.str] = None,
        help_text: typing.Optional[builtins.str] = None,
        hide_third_party_offers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        home_page_url: typing.Optional[builtins.str] = None,
        housekeeping_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        housekeeping_full_repack_period: typing.Optional[jsii.Number] = None,
        housekeeping_gc_period: typing.Optional[jsii.Number] = None,
        housekeeping_incremental_repack_period: typing.Optional[jsii.Number] = None,
        html_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        import_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        inactive_projects_delete_after_months: typing.Optional[jsii.Number] = None,
        inactive_projects_min_size_mb: typing.Optional[jsii.Number] = None,
        inactive_projects_send_warning_email_after_months: typing.Optional[jsii.Number] = None,
        in_product_marketing_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        invisible_captcha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        issues_create_limit: typing.Optional[jsii.Number] = None,
        keep_latest_artifact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        local_markdown_version: typing.Optional[jsii.Number] = None,
        mailgun_events_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mailgun_signing_key: typing.Optional[builtins.str] = None,
        maintenance_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        maintenance_mode_message: typing.Optional[builtins.str] = None,
        max_artifacts_size: typing.Optional[jsii.Number] = None,
        max_attachment_size: typing.Optional[jsii.Number] = None,
        max_export_size: typing.Optional[jsii.Number] = None,
        max_import_size: typing.Optional[jsii.Number] = None,
        max_number_of_repository_downloads: typing.Optional[jsii.Number] = None,
        max_number_of_repository_downloads_within_time_period: typing.Optional[jsii.Number] = None,
        max_pages_size: typing.Optional[jsii.Number] = None,
        max_personal_access_token_lifetime: typing.Optional[jsii.Number] = None,
        max_ssh_key_lifetime: typing.Optional[jsii.Number] = None,
        metrics_method_call_threshold: typing.Optional[jsii.Number] = None,
        mirror_available: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mirror_capacity_threshold: typing.Optional[jsii.Number] = None,
        mirror_max_capacity: typing.Optional[jsii.Number] = None,
        mirror_max_delay: typing.Optional[jsii.Number] = None,
        npm_package_requests_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        outbound_local_requests_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
        package_registry_cleanup_policies_worker_capacity: typing.Optional[jsii.Number] = None,
        pages_domain_verification_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_authentication_enabled_for_git: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_authentication_enabled_for_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_lowercase_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_number_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_symbol_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_uppercase_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        performance_bar_allowed_group_path: typing.Optional[builtins.str] = None,
        personal_access_token_prefix: typing.Optional[builtins.str] = None,
        pipeline_limit_per_project_user_sha: typing.Optional[jsii.Number] = None,
        plantuml_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        plantuml_url: typing.Optional[builtins.str] = None,
        polling_interval_multiplier: typing.Optional[jsii.Number] = None,
        project_export_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prometheus_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        protected_ci_variables: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        push_event_activities_limit: typing.Optional[jsii.Number] = None,
        push_event_hooks_limit: typing.Optional[jsii.Number] = None,
        pypi_package_requests_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rate_limiting_response_text: typing.Optional[builtins.str] = None,
        raw_blob_request_limit: typing.Optional[jsii.Number] = None,
        recaptcha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recaptcha_private_key: typing.Optional[builtins.str] = None,
        recaptcha_site_key: typing.Optional[builtins.str] = None,
        receive_max_input_size: typing.Optional[jsii.Number] = None,
        repository_checks_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        repository_size_limit: typing.Optional[jsii.Number] = None,
        repository_storages: typing.Optional[typing.Sequence[builtins.str]] = None,
        repository_storages_weighted: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
        require_admin_approval_after_user_signup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_two_factor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restricted_visibility_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
        rsa_key_restriction: typing.Optional[jsii.Number] = None,
        search_rate_limit: typing.Optional[jsii.Number] = None,
        search_rate_limit_unauthenticated: typing.Optional[jsii.Number] = None,
        send_user_confirmation_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        session_expire_delay: typing.Optional[jsii.Number] = None,
        shared_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_runners_minutes: typing.Optional[jsii.Number] = None,
        shared_runners_text: typing.Optional[builtins.str] = None,
        sidekiq_job_limiter_compression_threshold_bytes: typing.Optional[jsii.Number] = None,
        sidekiq_job_limiter_limit_bytes: typing.Optional[jsii.Number] = None,
        sidekiq_job_limiter_mode: typing.Optional[builtins.str] = None,
        sign_in_text: typing.Optional[builtins.str] = None,
        signup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        slack_app_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        slack_app_id: typing.Optional[builtins.str] = None,
        slack_app_secret: typing.Optional[builtins.str] = None,
        slack_app_signing_secret: typing.Optional[builtins.str] = None,
        slack_app_verification_token: typing.Optional[builtins.str] = None,
        snippet_size_limit: typing.Optional[jsii.Number] = None,
        snowplow_app_id: typing.Optional[builtins.str] = None,
        snowplow_collector_hostname: typing.Optional[builtins.str] = None,
        snowplow_cookie_domain: typing.Optional[builtins.str] = None,
        snowplow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sourcegraph_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sourcegraph_public_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sourcegraph_url: typing.Optional[builtins.str] = None,
        spam_check_api_key: typing.Optional[builtins.str] = None,
        spam_check_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        spam_check_endpoint_url: typing.Optional[builtins.str] = None,
        suggest_pipeline_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        terminal_max_session_time: typing.Optional[jsii.Number] = None,
        terms: typing.Optional[builtins.str] = None,
        throttle_authenticated_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_authenticated_api_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_authenticated_api_requests_per_period: typing.Optional[jsii.Number] = None,
        throttle_authenticated_packages_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_authenticated_packages_api_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_authenticated_packages_api_requests_per_period: typing.Optional[jsii.Number] = None,
        throttle_authenticated_web_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_authenticated_web_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_authenticated_web_requests_per_period: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_unauthenticated_api_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_api_requests_per_period: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_packages_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_unauthenticated_packages_api_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_packages_api_requests_per_period: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_web_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        throttle_unauthenticated_web_period_in_seconds: typing.Optional[jsii.Number] = None,
        throttle_unauthenticated_web_requests_per_period: typing.Optional[jsii.Number] = None,
        time_tracking_limit_to_hours: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        two_factor_grace_period: typing.Optional[jsii.Number] = None,
        unique_ips_limit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unique_ips_limit_per_user: typing.Optional[jsii.Number] = None,
        unique_ips_limit_time_window: typing.Optional[jsii.Number] = None,
        usage_ping_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_deactivation_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_default_external: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_default_internal_regex: typing.Optional[builtins.str] = None,
        user_oauth_applications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_show_add_ssh_key_message: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        web_ide_clientside_preview_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        whats_new_variant: typing.Optional[builtins.str] = None,
        wiki_page_max_content_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param abuse_notification_email: If set, abuse reports are sent to this address. Abuse reports are always available in the Admin Area. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#abuse_notification_email ApplicationSettings#abuse_notification_email}
        :param admin_mode: Require administrators to enable Admin Mode by re-authenticating for administrative tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#admin_mode ApplicationSettings#admin_mode}
        :param after_sign_out_path: Where to redirect users after logout. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#after_sign_out_path ApplicationSettings#after_sign_out_path}
        :param after_sign_up_text: Text shown to the user after signing up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#after_sign_up_text ApplicationSettings#after_sign_up_text}
        :param akismet_api_key: API key for Akismet spam protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#akismet_api_key ApplicationSettings#akismet_api_key}
        :param akismet_enabled: (If enabled, requires: akismet_api_key) Enable or disable Akismet spam protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#akismet_enabled ApplicationSettings#akismet_enabled}
        :param allow_group_owners_to_manage_ldap: Set to true to allow group owners to manage LDAP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#allow_group_owners_to_manage_ldap ApplicationSettings#allow_group_owners_to_manage_ldap}
        :param allow_local_requests_from_system_hooks: Allow requests to the local network from system hooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#allow_local_requests_from_system_hooks ApplicationSettings#allow_local_requests_from_system_hooks}
        :param allow_local_requests_from_web_hooks_and_services: Allow requests to the local network from web hooks and services. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#allow_local_requests_from_web_hooks_and_services ApplicationSettings#allow_local_requests_from_web_hooks_and_services}
        :param archive_builds_in_human_readable: Set the duration for which the jobs are considered as old and expired. After that time passes, the jobs are archived and no longer able to be retried. Make it empty to never expire jobs. It has to be no less than 1 day, for example: 15 days, 1 month, 2 years. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#archive_builds_in_human_readable ApplicationSettings#archive_builds_in_human_readable}
        :param asset_proxy_allowlist: Assets that match these domains are not proxied. Wildcards allowed. Your GitLab installation URL is automatically allowlisted. GitLab restart is required to apply changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_allowlist ApplicationSettings#asset_proxy_allowlist}
        :param asset_proxy_enabled: (If enabled, requires: asset_proxy_url) Enable proxying of assets. GitLab restart is required to apply changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_enabled ApplicationSettings#asset_proxy_enabled}
        :param asset_proxy_secret_key: Shared secret with the asset proxy server. GitLab restart is required to apply changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_secret_key ApplicationSettings#asset_proxy_secret_key}
        :param asset_proxy_url: URL of the asset proxy server. GitLab restart is required to apply changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_url ApplicationSettings#asset_proxy_url}
        :param authorized_keys_enabled: By default, we write to the authorized_keys file to support Git over SSH without additional configuration. GitLab can be optimized to authenticate SSH keys via the database file. Only disable this if you have configured your OpenSSH server to use the AuthorizedKeysCommand. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#authorized_keys_enabled ApplicationSettings#authorized_keys_enabled}
        :param auto_devops_domain: Specify a domain to use by default for every project’s Auto Review Apps and Auto Deploy stages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#auto_devops_domain ApplicationSettings#auto_devops_domain}
        :param auto_devops_enabled: Enable Auto DevOps for projects by default. It automatically builds, tests, and deploys applications based on a predefined CI/CD configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#auto_devops_enabled ApplicationSettings#auto_devops_enabled}
        :param automatic_purchased_storage_allocation: Enabling this permits automatic allocation of purchased storage in a namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#automatic_purchased_storage_allocation ApplicationSettings#automatic_purchased_storage_allocation}
        :param can_create_group: Indicates whether users can create top-level groups. Introduced in GitLab 15.5. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#can_create_group ApplicationSettings#can_create_group}
        :param check_namespace_plan: Enabling this makes only licensed EE features available to projects if the project namespace’s plan includes the feature or if the project is public. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#check_namespace_plan ApplicationSettings#check_namespace_plan}
        :param commit_email_hostname: Custom hostname (for private commit emails). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#commit_email_hostname ApplicationSettings#commit_email_hostname}
        :param container_expiration_policies_enable_historic_entries: Enable cleanup policies for all projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_expiration_policies_enable_historic_entries ApplicationSettings#container_expiration_policies_enable_historic_entries}
        :param container_registry_cleanup_tags_service_max_list_size: The maximum number of tags that can be deleted in a single execution of cleanup policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_cleanup_tags_service_max_list_size ApplicationSettings#container_registry_cleanup_tags_service_max_list_size}
        :param container_registry_delete_tags_service_timeout: The maximum time, in seconds, that the cleanup process can take to delete a batch of tags for cleanup policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_delete_tags_service_timeout ApplicationSettings#container_registry_delete_tags_service_timeout}
        :param container_registry_expiration_policies_caching: Caching during the execution of cleanup policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_expiration_policies_caching ApplicationSettings#container_registry_expiration_policies_caching}
        :param container_registry_expiration_policies_worker_capacity: Number of workers for cleanup policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_expiration_policies_worker_capacity ApplicationSettings#container_registry_expiration_policies_worker_capacity}
        :param container_registry_token_expire_delay: Container Registry token duration in minutes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_token_expire_delay ApplicationSettings#container_registry_token_expire_delay}
        :param deactivate_dormant_users: Enable automatic deactivation of dormant users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#deactivate_dormant_users ApplicationSettings#deactivate_dormant_users}
        :param default_artifacts_expire_in: Set the default expiration time for each job’s artifacts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_artifacts_expire_in ApplicationSettings#default_artifacts_expire_in}
        :param default_branch_name: Instance-level custom initial branch name (introduced in GitLab 13.2). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_branch_name ApplicationSettings#default_branch_name}
        :param default_branch_protection: Determine if developers can push to the default branch. Can take: 0 (not protected, both users with the Developer role or Maintainer role can push new commits and force push), 1 (partially protected, users with the Developer role or Maintainer role can push new commits, but cannot force push) or 2 (fully protected, users with the Developer or Maintainer role cannot push new commits, but users with the Developer or Maintainer role can; no one can force push) as a parameter. Default is 2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_branch_protection ApplicationSettings#default_branch_protection}
        :param default_ci_config_path: Default CI/CD configuration file and path for new projects (.gitlab-ci.yml if not set). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_ci_config_path ApplicationSettings#default_ci_config_path}
        :param default_group_visibility: What visibility level new groups receive. Can take private, internal and public as a parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_group_visibility ApplicationSettings#default_group_visibility}
        :param default_project_creation: Default project creation protection. Can take: 0 (No one), 1 (Maintainers) or 2 (Developers + Maintainers). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_project_creation ApplicationSettings#default_project_creation}
        :param default_projects_limit: Project limit per user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_projects_limit ApplicationSettings#default_projects_limit}
        :param default_project_visibility: What visibility level new projects receive. Can take private, internal and public as a parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_project_visibility ApplicationSettings#default_project_visibility}
        :param default_snippet_visibility: What visibility level new snippets receive. Can take private, internal and public as a parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_snippet_visibility ApplicationSettings#default_snippet_visibility}
        :param delayed_group_deletion: Enable delayed group deletion. Introduced in GitLab 15.0. From GitLab 15.1, disables and locks the group-level setting for delayed protect deletion when set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#delayed_group_deletion ApplicationSettings#delayed_group_deletion}
        :param delayed_project_deletion: Enable delayed project deletion by default in new groups. From GitLab 15.1, can only be enabled when delayed_group_deletion is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#delayed_project_deletion ApplicationSettings#delayed_project_deletion}
        :param delete_inactive_projects: Enable inactive project deletion feature. Introduced in GitLab 14.10. Became operational in GitLab 15.0 (with feature flag inactive_projects_deletion). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#delete_inactive_projects ApplicationSettings#delete_inactive_projects}
        :param deletion_adjourned_period: The number of days to wait before deleting a project or group that is marked for deletion. Value must be between 1 and 90. From GitLab 15.1, a hook on deletion_adjourned_period sets the period to 1 on every update, and sets both delayed_project_deletion and delayed_group_deletion to false if the period is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#deletion_adjourned_period ApplicationSettings#deletion_adjourned_period}
        :param diff_max_files: Maximum files in a diff. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#diff_max_files ApplicationSettings#diff_max_files}
        :param diff_max_lines: Maximum lines in a diff. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#diff_max_lines ApplicationSettings#diff_max_lines}
        :param diff_max_patch_bytes: Maximum diff patch size, in bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#diff_max_patch_bytes ApplicationSettings#diff_max_patch_bytes}
        :param disabled_oauth_sign_in_sources: Disabled OAuth sign-in sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#disabled_oauth_sign_in_sources ApplicationSettings#disabled_oauth_sign_in_sources}
        :param disable_feed_token: Disable display of RSS/Atom and calendar feed tokens (introduced in GitLab 13.7). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#disable_feed_token ApplicationSettings#disable_feed_token}
        :param dns_rebinding_protection_enabled: Enforce DNS rebinding attack protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#dns_rebinding_protection_enabled ApplicationSettings#dns_rebinding_protection_enabled}
        :param domain_allowlist: Force people to use only corporate emails for sign-up. Null means there is no restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#domain_allowlist ApplicationSettings#domain_allowlist}
        :param domain_denylist: Users with email addresses that match these domains cannot sign up. Wildcards allowed. Use separate lines for multiple entries. Ex: domain.com, *.domain.com. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#domain_denylist ApplicationSettings#domain_denylist}
        :param domain_denylist_enabled: (If enabled, requires: domain_denylist) Allows blocking sign-ups from emails from specific domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#domain_denylist_enabled ApplicationSettings#domain_denylist_enabled}
        :param dsa_key_restriction: The minimum allowed bit length of an uploaded DSA key. 0 means no restriction. -1 disables DSA keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#dsa_key_restriction ApplicationSettings#dsa_key_restriction}
        :param ecdsa_key_restriction: The minimum allowed curve size (in bits) of an uploaded ECDSA key. 0 means no restriction. -1 disables ECDSA keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ecdsa_key_restriction ApplicationSettings#ecdsa_key_restriction}
        :param ecdsa_sk_key_restriction: The minimum allowed curve size (in bits) of an uploaded ECDSA_SK key. 0 means no restriction. -1 disables ECDSA_SK keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ecdsa_sk_key_restriction ApplicationSettings#ecdsa_sk_key_restriction}
        :param ed25519_key_restriction: The minimum allowed curve size (in bits) of an uploaded ED25519 key. 0 means no restriction. -1 disables ED25519 keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ed25519_key_restriction ApplicationSettings#ed25519_key_restriction}
        :param ed25519_sk_key_restriction: The minimum allowed curve size (in bits) of an uploaded ED25519_SK key. 0 means no restriction. -1 disables ED25519_SK keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ed25519_sk_key_restriction ApplicationSettings#ed25519_sk_key_restriction}
        :param eks_access_key_id: AWS IAM access key ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_access_key_id ApplicationSettings#eks_access_key_id}
        :param eks_account_id: Amazon account ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_account_id ApplicationSettings#eks_account_id}
        :param eks_integration_enabled: Enable integration with Amazon EKS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_integration_enabled ApplicationSettings#eks_integration_enabled}
        :param eks_secret_access_key: AWS IAM secret access key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_secret_access_key ApplicationSettings#eks_secret_access_key}
        :param elasticsearch_aws: Enable the use of AWS hosted Elasticsearch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws ApplicationSettings#elasticsearch_aws}
        :param elasticsearch_aws_access_key: AWS IAM access key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws_access_key ApplicationSettings#elasticsearch_aws_access_key}
        :param elasticsearch_aws_region: The AWS region the Elasticsearch domain is configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws_region ApplicationSettings#elasticsearch_aws_region}
        :param elasticsearch_aws_secret_access_key: AWS IAM secret access key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws_secret_access_key ApplicationSettings#elasticsearch_aws_secret_access_key}
        :param elasticsearch_indexed_field_length_limit: Maximum size of text fields to index by Elasticsearch. 0 value means no limit. This does not apply to repository and wiki indexing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_indexed_field_length_limit ApplicationSettings#elasticsearch_indexed_field_length_limit}
        :param elasticsearch_indexed_file_size_limit_kb: Maximum size of repository and wiki files that are indexed by Elasticsearch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_indexed_file_size_limit_kb ApplicationSettings#elasticsearch_indexed_file_size_limit_kb}
        :param elasticsearch_indexing: Enable Elasticsearch indexing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_indexing ApplicationSettings#elasticsearch_indexing}
        :param elasticsearch_limit_indexing: Limit Elasticsearch to index certain namespaces and projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_limit_indexing ApplicationSettings#elasticsearch_limit_indexing}
        :param elasticsearch_max_bulk_concurrency: Maximum concurrency of Elasticsearch bulk requests per indexing operation. This only applies to repository indexing operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_max_bulk_concurrency ApplicationSettings#elasticsearch_max_bulk_concurrency}
        :param elasticsearch_max_bulk_size_mb: Maximum size of Elasticsearch bulk indexing requests in MB. This only applies to repository indexing operations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_max_bulk_size_mb ApplicationSettings#elasticsearch_max_bulk_size_mb}
        :param elasticsearch_namespace_ids: The namespaces to index via Elasticsearch if elasticsearch_limit_indexing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_namespace_ids ApplicationSettings#elasticsearch_namespace_ids}
        :param elasticsearch_password: The password of your Elasticsearch instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_password ApplicationSettings#elasticsearch_password}
        :param elasticsearch_project_ids: The projects to index via Elasticsearch if elasticsearch_limit_indexing is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_project_ids ApplicationSettings#elasticsearch_project_ids}
        :param elasticsearch_search: Enable Elasticsearch search. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_search ApplicationSettings#elasticsearch_search}
        :param elasticsearch_url: The URL to use for connecting to Elasticsearch. Use a comma-separated list to support cluster (for example, http://localhost:9200, http://localhost:9201). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_url ApplicationSettings#elasticsearch_url}
        :param elasticsearch_username: The username of your Elasticsearch instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_username ApplicationSettings#elasticsearch_username}
        :param email_additional_text: Additional text added to the bottom of every email for legal/auditing/compliance reasons. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#email_additional_text ApplicationSettings#email_additional_text}
        :param email_author_in_body: Some email servers do not support overriding the email sender name. Enable this option to include the name of the author of the issue, merge request or comment in the email body instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#email_author_in_body ApplicationSettings#email_author_in_body}
        :param enabled_git_access_protocol: Enabled protocols for Git access. Allowed values are: ssh, http, and nil to allow both protocols. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#enabled_git_access_protocol ApplicationSettings#enabled_git_access_protocol}
        :param enforce_namespace_storage_limit: Enabling this permits enforcement of namespace storage limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#enforce_namespace_storage_limit ApplicationSettings#enforce_namespace_storage_limit}
        :param enforce_terms: (If enabled, requires: terms) Enforce application ToS to all users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#enforce_terms ApplicationSettings#enforce_terms}
        :param external_auth_client_cert: (If enabled, requires: external_auth_client_key) The certificate to use to authenticate with the external authorization service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_auth_client_cert ApplicationSettings#external_auth_client_cert}
        :param external_auth_client_key: Private key for the certificate when authentication is required for the external authorization service, this is encrypted when stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_auth_client_key ApplicationSettings#external_auth_client_key}
        :param external_auth_client_key_pass: Passphrase to use for the private key when authenticating with the external service this is encrypted when stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_auth_client_key_pass ApplicationSettings#external_auth_client_key_pass}
        :param external_authorization_service_default_label: The default classification label to use when requesting authorization and no classification label has been specified on the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_default_label ApplicationSettings#external_authorization_service_default_label}
        :param external_authorization_service_enabled: (If enabled, requires: external_authorization_service_default_label, external_authorization_service_timeout and external_authorization_service_url) Enable using an external authorization service for accessing projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_enabled ApplicationSettings#external_authorization_service_enabled}
        :param external_authorization_service_timeout: The timeout after which an authorization request is aborted, in seconds. When a request times out, access is denied to the user. (min: 0.001, max: 10, step: 0.001). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_timeout ApplicationSettings#external_authorization_service_timeout}
        :param external_authorization_service_url: URL to which authorization requests are directed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_url ApplicationSettings#external_authorization_service_url}
        :param external_pipeline_validation_service_timeout: How long to wait for a response from the pipeline validation service. Assumes OK if it times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_pipeline_validation_service_timeout ApplicationSettings#external_pipeline_validation_service_timeout}
        :param external_pipeline_validation_service_token: Optional. Token to include as the X-Gitlab-Token header in requests to the URL in external_pipeline_validation_service_url. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_pipeline_validation_service_token ApplicationSettings#external_pipeline_validation_service_token}
        :param external_pipeline_validation_service_url: URL to use for pipeline validation requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_pipeline_validation_service_url ApplicationSettings#external_pipeline_validation_service_url}
        :param file_template_project_id: The ID of a project to load custom file templates from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#file_template_project_id ApplicationSettings#file_template_project_id}
        :param first_day_of_week: Start day of the week for calendar views and date pickers. Valid values are 0 for Sunday, 1 for Monday, and 6 for Saturday. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#first_day_of_week ApplicationSettings#first_day_of_week}
        :param geo_node_allowed_ips: Comma-separated list of IPs and CIDRs of allowed secondary nodes. For example, 1.1.1.1, 2.2.2.0/24. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#geo_node_allowed_ips ApplicationSettings#geo_node_allowed_ips}
        :param geo_status_timeout: The amount of seconds after which a request to get a secondary node status times out. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#geo_status_timeout ApplicationSettings#geo_status_timeout}
        :param gitaly_timeout_default: Default Gitaly timeout, in seconds. This timeout is not enforced for Git fetch/push operations or Sidekiq jobs. Set to 0 to disable timeouts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gitaly_timeout_default ApplicationSettings#gitaly_timeout_default}
        :param gitaly_timeout_fast: Gitaly fast operation timeout, in seconds. Some Gitaly operations are expected to be fast. If they exceed this threshold, there may be a problem with a storage shard and ‘failing fast’ can help maintain the stability of the GitLab instance. Set to 0 to disable timeouts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gitaly_timeout_fast ApplicationSettings#gitaly_timeout_fast}
        :param gitaly_timeout_medium: Medium Gitaly timeout, in seconds. This should be a value between the Fast and the Default timeout. Set to 0 to disable timeouts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gitaly_timeout_medium ApplicationSettings#gitaly_timeout_medium}
        :param git_rate_limit_users_allowlist: List of usernames excluded from Git anti-abuse rate limits. Maximum: 100 usernames. Introduced in GitLab 15.2. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#git_rate_limit_users_allowlist ApplicationSettings#git_rate_limit_users_allowlist}
        :param git_two_factor_session_expiry: Maximum duration (in minutes) of a session for Git operations when 2FA is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#git_two_factor_session_expiry ApplicationSettings#git_two_factor_session_expiry}
        :param grafana_enabled: Enable Grafana. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#grafana_enabled ApplicationSettings#grafana_enabled}
        :param grafana_url: Grafana URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#grafana_url ApplicationSettings#grafana_url}
        :param gravatar_enabled: Enable Gravatar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gravatar_enabled ApplicationSettings#gravatar_enabled}
        :param group_owners_can_manage_default_branch_protection: Prevent overrides of default branch protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#group_owners_can_manage_default_branch_protection ApplicationSettings#group_owners_can_manage_default_branch_protection}
        :param hashed_storage_enabled: Create new projects using hashed storage paths: Enable immutable, hash-based paths and repository names to store repositories on disk. This prevents repositories from having to be moved or renamed when the Project URL changes and may improve disk I/O performance. (Always enabled in GitLab versions 13.0 and later, configuration is scheduled for removal in 14.0). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#hashed_storage_enabled ApplicationSettings#hashed_storage_enabled}
        :param help_page_hide_commercial_content: Hide marketing-related entries from help. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_page_hide_commercial_content ApplicationSettings#help_page_hide_commercial_content}
        :param help_page_support_url: Alternate support URL for help page and help dropdown. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_page_support_url ApplicationSettings#help_page_support_url}
        :param help_page_text: Custom text displayed on the help page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_page_text ApplicationSettings#help_page_text}
        :param help_text: GitLab server administrator information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_text ApplicationSettings#help_text}
        :param hide_third_party_offers: Do not display offers from third parties in GitLab. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#hide_third_party_offers ApplicationSettings#hide_third_party_offers}
        :param home_page_url: Redirect to this URL when not logged in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#home_page_url ApplicationSettings#home_page_url}
        :param housekeeping_enabled: (If enabled, requires: housekeeping_bitmaps_enabled, housekeeping_full_repack_period, housekeeping_gc_period, and housekeeping_incremental_repack_period) Enable or disable Git housekeeping. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_enabled ApplicationSettings#housekeeping_enabled}
        :param housekeeping_full_repack_period: Number of Git pushes after which an incremental git repack is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_full_repack_period ApplicationSettings#housekeeping_full_repack_period}
        :param housekeeping_gc_period: Number of Git pushes after which git gc is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_gc_period ApplicationSettings#housekeeping_gc_period}
        :param housekeeping_incremental_repack_period: Number of Git pushes after which an incremental git repack is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_incremental_repack_period ApplicationSettings#housekeeping_incremental_repack_period}
        :param html_emails_enabled: Enable HTML emails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#html_emails_enabled ApplicationSettings#html_emails_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#id ApplicationSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_sources: Sources to allow project import from. Valid values are: ``github``, ``bitbucket``, ``bitbucket_server``, ``fogbugz``, ``git``, ``gitlab_project``, ``gitea``, ``manifest``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#import_sources ApplicationSettings#import_sources}
        :param inactive_projects_delete_after_months: If delete_inactive_projects is true, the time (in months) to wait before deleting inactive projects. Introduced in GitLab 14.10. Became operational in GitLab 15.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#inactive_projects_delete_after_months ApplicationSettings#inactive_projects_delete_after_months}
        :param inactive_projects_min_size_mb: If delete_inactive_projects is true, the minimum repository size for projects to be checked for inactivity. Introduced in GitLab 14.10. Became operational in GitLab 15.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#inactive_projects_min_size_mb ApplicationSettings#inactive_projects_min_size_mb}
        :param inactive_projects_send_warning_email_after_months: If delete_inactive_projects is true, sets the time (in months) to wait before emailing maintainers that the project is scheduled be deleted because it is inactive. Introduced in GitLab 14.10. Became operational in GitLab 15.0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#inactive_projects_send_warning_email_after_months ApplicationSettings#inactive_projects_send_warning_email_after_months}
        :param in_product_marketing_emails_enabled: Enable in-product marketing emails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#in_product_marketing_emails_enabled ApplicationSettings#in_product_marketing_emails_enabled}
        :param invisible_captcha_enabled: Enable Invisible CAPTCHA spam detection during sign-up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#invisible_captcha_enabled ApplicationSettings#invisible_captcha_enabled}
        :param issues_create_limit: Max number of issue creation requests per minute per user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#issues_create_limit ApplicationSettings#issues_create_limit}
        :param keep_latest_artifact: Prevent the deletion of the artifacts from the most recent successful jobs, regardless of the expiry time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#keep_latest_artifact ApplicationSettings#keep_latest_artifact}
        :param local_markdown_version: Increase this value when any cached Markdown should be invalidated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#local_markdown_version ApplicationSettings#local_markdown_version}
        :param mailgun_events_enabled: Enable Mailgun event receiver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mailgun_events_enabled ApplicationSettings#mailgun_events_enabled}
        :param mailgun_signing_key: The Mailgun HTTP webhook signing key for receiving events from webhook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mailgun_signing_key ApplicationSettings#mailgun_signing_key}
        :param maintenance_mode: When instance is in maintenance mode, non-administrative users can sign in with read-only access and make read-only API requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#maintenance_mode ApplicationSettings#maintenance_mode}
        :param maintenance_mode_message: Message displayed when instance is in maintenance mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#maintenance_mode_message ApplicationSettings#maintenance_mode_message}
        :param max_artifacts_size: Maximum artifacts size in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_artifacts_size ApplicationSettings#max_artifacts_size}
        :param max_attachment_size: Limit attachment size in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_attachment_size ApplicationSettings#max_attachment_size}
        :param max_export_size: Maximum export size in MB. 0 for unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_export_size ApplicationSettings#max_export_size}
        :param max_import_size: Maximum import size in MB. 0 for unlimited. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_import_size ApplicationSettings#max_import_size}
        :param max_number_of_repository_downloads: Maximum number of unique repositories a user can download in the specified time period before they are banned. Maximum: 10,000 repositories. Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_number_of_repository_downloads ApplicationSettings#max_number_of_repository_downloads}
        :param max_number_of_repository_downloads_within_time_period: Reporting time period (in seconds). Maximum: 864000 seconds (10 days). Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_number_of_repository_downloads_within_time_period ApplicationSettings#max_number_of_repository_downloads_within_time_period}
        :param max_pages_size: Maximum size of pages repositories in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_pages_size ApplicationSettings#max_pages_size}
        :param max_personal_access_token_lifetime: Maximum allowable lifetime for access tokens in days. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_personal_access_token_lifetime ApplicationSettings#max_personal_access_token_lifetime}
        :param max_ssh_key_lifetime: Maximum allowable lifetime for SSH keys in days. Introduced in GitLab 14.6. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_ssh_key_lifetime ApplicationSettings#max_ssh_key_lifetime}
        :param metrics_method_call_threshold: A method call is only tracked when it takes longer than the given amount of milliseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#metrics_method_call_threshold ApplicationSettings#metrics_method_call_threshold}
        :param mirror_available: Allow repository mirroring to configured by project Maintainers. If disabled, only Administrators can configure repository mirroring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_available ApplicationSettings#mirror_available}
        :param mirror_capacity_threshold: Minimum capacity to be available before scheduling more mirrors preemptively. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_capacity_threshold ApplicationSettings#mirror_capacity_threshold}
        :param mirror_max_capacity: Maximum number of mirrors that can be synchronizing at the same time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_max_capacity ApplicationSettings#mirror_max_capacity}
        :param mirror_max_delay: Maximum time (in minutes) between updates that a mirror can have when scheduled to synchronize. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_max_delay ApplicationSettings#mirror_max_delay}
        :param npm_package_requests_forwarding: Use npmjs.org as a default remote repository when the package is not found in the GitLab Package Registry for npm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#npm_package_requests_forwarding ApplicationSettings#npm_package_requests_forwarding}
        :param outbound_local_requests_whitelist: Define a list of trusted domains or IP addresses to which local requests are allowed when local requests for hooks and services are disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#outbound_local_requests_whitelist ApplicationSettings#outbound_local_requests_whitelist}
        :param package_registry_cleanup_policies_worker_capacity: Number of workers assigned to the packages cleanup policies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#package_registry_cleanup_policies_worker_capacity ApplicationSettings#package_registry_cleanup_policies_worker_capacity}
        :param pages_domain_verification_enabled: Require users to prove ownership of custom domains. Domain verification is an essential security measure for public GitLab sites. Users are required to demonstrate they control a domain before it is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#pages_domain_verification_enabled ApplicationSettings#pages_domain_verification_enabled}
        :param password_authentication_enabled_for_git: Enable authentication for Git over HTTP(S) via a GitLab account password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_authentication_enabled_for_git ApplicationSettings#password_authentication_enabled_for_git}
        :param password_authentication_enabled_for_web: Enable authentication for the web interface via a GitLab account password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_authentication_enabled_for_web ApplicationSettings#password_authentication_enabled_for_web}
        :param password_lowercase_required: Indicates whether passwords require at least one lowercase letter. Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_lowercase_required ApplicationSettings#password_lowercase_required}
        :param password_number_required: Indicates whether passwords require at least one number. Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_number_required ApplicationSettings#password_number_required}
        :param password_symbol_required: Indicates whether passwords require at least one symbol character. Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_symbol_required ApplicationSettings#password_symbol_required}
        :param password_uppercase_required: Indicates whether passwords require at least one uppercase letter. Introduced in GitLab 15.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_uppercase_required ApplicationSettings#password_uppercase_required}
        :param performance_bar_allowed_group_path: Path of the group that is allowed to toggle the performance bar. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#performance_bar_allowed_group_path ApplicationSettings#performance_bar_allowed_group_path}
        :param personal_access_token_prefix: Prefix for all generated personal access tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#personal_access_token_prefix ApplicationSettings#personal_access_token_prefix}
        :param pipeline_limit_per_project_user_sha: Maximum number of pipeline creation requests per minute per user and commit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#pipeline_limit_per_project_user_sha ApplicationSettings#pipeline_limit_per_project_user_sha}
        :param plantuml_enabled: (If enabled, requires: plantuml_url) Enable PlantUML integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#plantuml_enabled ApplicationSettings#plantuml_enabled}
        :param plantuml_url: The PlantUML instance URL for integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#plantuml_url ApplicationSettings#plantuml_url}
        :param polling_interval_multiplier: Interval multiplier used by endpoints that perform polling. Set to 0 to disable polling. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#polling_interval_multiplier ApplicationSettings#polling_interval_multiplier}
        :param project_export_enabled: Enable project export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#project_export_enabled ApplicationSettings#project_export_enabled}
        :param prometheus_metrics_enabled: Enable Prometheus metrics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#prometheus_metrics_enabled ApplicationSettings#prometheus_metrics_enabled}
        :param protected_ci_variables: CI/CD variables are protected by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#protected_ci_variables ApplicationSettings#protected_ci_variables}
        :param push_event_activities_limit: Number of changes (branches or tags) in a single push to determine whether individual push events or bulk push events are created. Bulk push events are created if it surpasses that value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#push_event_activities_limit ApplicationSettings#push_event_activities_limit}
        :param push_event_hooks_limit: Number of changes (branches or tags) in a single push to determine whether webhooks and services fire or not. Webhooks and services aren’t submitted if it surpasses that value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#push_event_hooks_limit ApplicationSettings#push_event_hooks_limit}
        :param pypi_package_requests_forwarding: Use pypi.org as a default remote repository when the package is not found in the GitLab Package Registry for PyPI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#pypi_package_requests_forwarding ApplicationSettings#pypi_package_requests_forwarding}
        :param rate_limiting_response_text: When rate limiting is enabled via the throttle_* settings, send this plain text response when a rate limit is exceeded. ‘Retry later’ is sent if this is blank. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#rate_limiting_response_text ApplicationSettings#rate_limiting_response_text}
        :param raw_blob_request_limit: Max number of requests per minute for each raw path. To disable throttling set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#raw_blob_request_limit ApplicationSettings#raw_blob_request_limit}
        :param recaptcha_enabled: (If enabled, requires: recaptcha_private_key and recaptcha_site_key) Enable reCAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#recaptcha_enabled ApplicationSettings#recaptcha_enabled}
        :param recaptcha_private_key: Private key for reCAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#recaptcha_private_key ApplicationSettings#recaptcha_private_key}
        :param recaptcha_site_key: Site key for reCAPTCHA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#recaptcha_site_key ApplicationSettings#recaptcha_site_key}
        :param receive_max_input_size: Maximum push size (MB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#receive_max_input_size ApplicationSettings#receive_max_input_size}
        :param repository_checks_enabled: GitLab periodically runs git fsck in all project and wiki repositories to look for silent disk corruption issues. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_checks_enabled ApplicationSettings#repository_checks_enabled}
        :param repository_size_limit: Size limit per repository (MB). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_size_limit ApplicationSettings#repository_size_limit}
        :param repository_storages: (GitLab 13.0 and earlier) List of names of enabled storage paths, taken from gitlab.yml. New projects are created in one of these stores, chosen at random. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_storages ApplicationSettings#repository_storages}
        :param repository_storages_weighted: (GitLab 13.1 and later) Hash of names of taken from gitlab.yml to weights. New projects are created in one of these stores, chosen by a weighted random selection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_storages_weighted ApplicationSettings#repository_storages_weighted}
        :param require_admin_approval_after_user_signup: When enabled, any user that signs up for an account using the registration form is placed under a Pending approval state and has to be explicitly approved by an administrator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#require_admin_approval_after_user_signup ApplicationSettings#require_admin_approval_after_user_signup}
        :param require_two_factor_authentication: (If enabled, requires: two_factor_grace_period) Require all users to set up Two-factor authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#require_two_factor_authentication ApplicationSettings#require_two_factor_authentication}
        :param restricted_visibility_levels: Selected levels cannot be used by non-Administrator users for groups, projects or snippets. Can take private, internal and public as a parameter. Null means there is no restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#restricted_visibility_levels ApplicationSettings#restricted_visibility_levels}
        :param rsa_key_restriction: The minimum allowed bit length of an uploaded RSA key. 0 means no restriction. -1 disables RSA keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#rsa_key_restriction ApplicationSettings#rsa_key_restriction}
        :param search_rate_limit: Max number of requests per minute for performing a search while authenticated. To disable throttling set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#search_rate_limit ApplicationSettings#search_rate_limit}
        :param search_rate_limit_unauthenticated: Max number of requests per minute for performing a search while unauthenticated. To disable throttling set to 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#search_rate_limit_unauthenticated ApplicationSettings#search_rate_limit_unauthenticated}
        :param send_user_confirmation_email: Send confirmation email on sign-up. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#send_user_confirmation_email ApplicationSettings#send_user_confirmation_email}
        :param session_expire_delay: Session duration in minutes. GitLab restart is required to apply changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#session_expire_delay ApplicationSettings#session_expire_delay}
        :param shared_runners_enabled: (If enabled, requires: shared_runners_text and shared_runners_minutes) Enable shared runners for new projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#shared_runners_enabled ApplicationSettings#shared_runners_enabled}
        :param shared_runners_minutes: Set the maximum number of CI/CD minutes that a group can use on shared runners per month. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#shared_runners_minutes ApplicationSettings#shared_runners_minutes}
        :param shared_runners_text: Shared runners text. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#shared_runners_text ApplicationSettings#shared_runners_text}
        :param sidekiq_job_limiter_compression_threshold_bytes: The threshold in bytes at which Sidekiq jobs are compressed before being stored in Redis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sidekiq_job_limiter_compression_threshold_bytes ApplicationSettings#sidekiq_job_limiter_compression_threshold_bytes}
        :param sidekiq_job_limiter_limit_bytes: The threshold in bytes at which Sidekiq jobs are rejected. 0 means do not reject any job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sidekiq_job_limiter_limit_bytes ApplicationSettings#sidekiq_job_limiter_limit_bytes}
        :param sidekiq_job_limiter_mode: track or compress. Sets the behavior for Sidekiq job size limits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sidekiq_job_limiter_mode ApplicationSettings#sidekiq_job_limiter_mode}
        :param sign_in_text: Text on the login page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sign_in_text ApplicationSettings#sign_in_text}
        :param signup_enabled: Enable registration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#signup_enabled ApplicationSettings#signup_enabled}
        :param slack_app_enabled: (If enabled, requires: slack_app_id, slack_app_secret and slack_app_secret) Enable Slack app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_enabled ApplicationSettings#slack_app_enabled}
        :param slack_app_id: The app ID of the Slack-app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_id ApplicationSettings#slack_app_id}
        :param slack_app_secret: The app secret of the Slack-app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_secret ApplicationSettings#slack_app_secret}
        :param slack_app_signing_secret: The signing secret of the Slack-app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_signing_secret ApplicationSettings#slack_app_signing_secret}
        :param slack_app_verification_token: The verification token of the Slack-app. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_verification_token ApplicationSettings#slack_app_verification_token}
        :param snippet_size_limit: Max snippet content size in bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snippet_size_limit ApplicationSettings#snippet_size_limit}
        :param snowplow_app_id: The Snowplow site name / application ID. (for example, gitlab). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_app_id ApplicationSettings#snowplow_app_id}
        :param snowplow_collector_hostname: The Snowplow collector hostname. (for example, snowplow.trx.gitlab.net). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_collector_hostname ApplicationSettings#snowplow_collector_hostname}
        :param snowplow_cookie_domain: The Snowplow cookie domain. (for example, .gitlab.com). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_cookie_domain ApplicationSettings#snowplow_cookie_domain}
        :param snowplow_enabled: Enable snowplow tracking. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_enabled ApplicationSettings#snowplow_enabled}
        :param sourcegraph_enabled: Enables Sourcegraph integration. If enabled, requires sourcegraph_url. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sourcegraph_enabled ApplicationSettings#sourcegraph_enabled}
        :param sourcegraph_public_only: Blocks Sourcegraph from being loaded on private and internal projects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sourcegraph_public_only ApplicationSettings#sourcegraph_public_only}
        :param sourcegraph_url: The Sourcegraph instance URL for integration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sourcegraph_url ApplicationSettings#sourcegraph_url}
        :param spam_check_api_key: API key used by GitLab for accessing the Spam Check service endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#spam_check_api_key ApplicationSettings#spam_check_api_key}
        :param spam_check_endpoint_enabled: Enables spam checking using external Spam Check API endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#spam_check_endpoint_enabled ApplicationSettings#spam_check_endpoint_enabled}
        :param spam_check_endpoint_url: URL of the external Spamcheck service endpoint. Valid URI schemes are grpc or tls. Specifying tls forces communication to be encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#spam_check_endpoint_url ApplicationSettings#spam_check_endpoint_url}
        :param suggest_pipeline_enabled: Enable pipeline suggestion banner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#suggest_pipeline_enabled ApplicationSettings#suggest_pipeline_enabled}
        :param terminal_max_session_time: Maximum time for web terminal websocket connection (in seconds). Set to 0 for unlimited time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#terminal_max_session_time ApplicationSettings#terminal_max_session_time}
        :param terms: (Required by: enforce_terms) Markdown content for the ToS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#terms ApplicationSettings#terms}
        :param throttle_authenticated_api_enabled: (If enabled, requires: throttle_authenticated_api_period_in_seconds and throttle_authenticated_api_requests_per_period) Enable authenticated API request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_api_enabled ApplicationSettings#throttle_authenticated_api_enabled}
        :param throttle_authenticated_api_period_in_seconds: Rate limit period (in seconds). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_api_period_in_seconds ApplicationSettings#throttle_authenticated_api_period_in_seconds}
        :param throttle_authenticated_api_requests_per_period: Maximum requests per period per user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_api_requests_per_period ApplicationSettings#throttle_authenticated_api_requests_per_period}
        :param throttle_authenticated_packages_api_enabled: (If enabled, requires: throttle_authenticated_packages_api_period_in_seconds and throttle_authenticated_packages_api_requests_per_period) Enable authenticated API request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_packages_api_enabled ApplicationSettings#throttle_authenticated_packages_api_enabled}
        :param throttle_authenticated_packages_api_period_in_seconds: Rate limit period (in seconds). View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_packages_api_period_in_seconds ApplicationSettings#throttle_authenticated_packages_api_period_in_seconds}
        :param throttle_authenticated_packages_api_requests_per_period: Maximum requests per period per user. View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_packages_api_requests_per_period ApplicationSettings#throttle_authenticated_packages_api_requests_per_period}
        :param throttle_authenticated_web_enabled: (If enabled, requires: throttle_authenticated_web_period_in_seconds and throttle_authenticated_web_requests_per_period) Enable authenticated web request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_web_enabled ApplicationSettings#throttle_authenticated_web_enabled}
        :param throttle_authenticated_web_period_in_seconds: Rate limit period (in seconds). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_web_period_in_seconds ApplicationSettings#throttle_authenticated_web_period_in_seconds}
        :param throttle_authenticated_web_requests_per_period: Maximum requests per period per user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_web_requests_per_period ApplicationSettings#throttle_authenticated_web_requests_per_period}
        :param throttle_unauthenticated_api_enabled: (If enabled, requires: throttle_unauthenticated_api_period_in_seconds and throttle_unauthenticated_api_requests_per_period) Enable unauthenticated API request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_api_enabled ApplicationSettings#throttle_unauthenticated_api_enabled}
        :param throttle_unauthenticated_api_period_in_seconds: Rate limit period in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_api_period_in_seconds ApplicationSettings#throttle_unauthenticated_api_period_in_seconds}
        :param throttle_unauthenticated_api_requests_per_period: Max requests per period per IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_api_requests_per_period ApplicationSettings#throttle_unauthenticated_api_requests_per_period}
        :param throttle_unauthenticated_packages_api_enabled: (If enabled, requires: throttle_unauthenticated_packages_api_period_in_seconds and throttle_unauthenticated_packages_api_requests_per_period) Enable authenticated API request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_packages_api_enabled ApplicationSettings#throttle_unauthenticated_packages_api_enabled}
        :param throttle_unauthenticated_packages_api_period_in_seconds: Rate limit period (in seconds). View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_packages_api_period_in_seconds ApplicationSettings#throttle_unauthenticated_packages_api_period_in_seconds}
        :param throttle_unauthenticated_packages_api_requests_per_period: Maximum requests per period per user. View Package Registry rate limits for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_packages_api_requests_per_period ApplicationSettings#throttle_unauthenticated_packages_api_requests_per_period}
        :param throttle_unauthenticated_web_enabled: (If enabled, requires: throttle_unauthenticated_web_period_in_seconds and throttle_unauthenticated_web_requests_per_period) Enable unauthenticated web request rate limit. Helps reduce request volume (for example, from crawlers or abusive bots). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_web_enabled ApplicationSettings#throttle_unauthenticated_web_enabled}
        :param throttle_unauthenticated_web_period_in_seconds: Rate limit period in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_web_period_in_seconds ApplicationSettings#throttle_unauthenticated_web_period_in_seconds}
        :param throttle_unauthenticated_web_requests_per_period: Max requests per period per IP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_web_requests_per_period ApplicationSettings#throttle_unauthenticated_web_requests_per_period}
        :param time_tracking_limit_to_hours: Limit display of time tracking units to hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#time_tracking_limit_to_hours ApplicationSettings#time_tracking_limit_to_hours}
        :param two_factor_grace_period: Amount of time (in hours) that users are allowed to skip forced configuration of two-factor authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#two_factor_grace_period ApplicationSettings#two_factor_grace_period}
        :param unique_ips_limit_enabled: (If enabled, requires: unique_ips_limit_per_user and unique_ips_limit_time_window) Limit sign in from multiple IPs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#unique_ips_limit_enabled ApplicationSettings#unique_ips_limit_enabled}
        :param unique_ips_limit_per_user: Maximum number of IPs per user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#unique_ips_limit_per_user ApplicationSettings#unique_ips_limit_per_user}
        :param unique_ips_limit_time_window: How many seconds an IP is counted towards the limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#unique_ips_limit_time_window ApplicationSettings#unique_ips_limit_time_window}
        :param usage_ping_enabled: Every week GitLab reports license usage back to GitLab, Inc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#usage_ping_enabled ApplicationSettings#usage_ping_enabled}
        :param user_deactivation_emails_enabled: Send an email to users upon account deactivation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_deactivation_emails_enabled ApplicationSettings#user_deactivation_emails_enabled}
        :param user_default_external: Newly registered users are external by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_default_external ApplicationSettings#user_default_external}
        :param user_default_internal_regex: Specify an email address regex pattern to identify default internal users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_default_internal_regex ApplicationSettings#user_default_internal_regex}
        :param user_oauth_applications: Allow users to register any application to use GitLab as an OAuth provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_oauth_applications ApplicationSettings#user_oauth_applications}
        :param user_show_add_ssh_key_message: When set to false disable the You won't be able to pull or push project code via SSH warning shown to users with no uploaded SSH key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_show_add_ssh_key_message ApplicationSettings#user_show_add_ssh_key_message}
        :param version_check_enabled: Let GitLab inform you when an update is available. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#version_check_enabled ApplicationSettings#version_check_enabled}
        :param web_ide_clientside_preview_enabled: Live Preview (allow live previews of JavaScript projects in the Web IDE using CodeSandbox Live Preview). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#web_ide_clientside_preview_enabled ApplicationSettings#web_ide_clientside_preview_enabled}
        :param whats_new_variant: What’s new variant, possible values: all_tiers, current_tier, and disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#whats_new_variant ApplicationSettings#whats_new_variant}
        :param wiki_page_max_content_bytes: Maximum wiki page content size in bytes. The minimum value is 1024 bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#wiki_page_max_content_bytes ApplicationSettings#wiki_page_max_content_bytes}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c50b86976e6a321d315529ec7b5d8fe1bc23f479e146940bc53976f68530f641)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument abuse_notification_email", value=abuse_notification_email, expected_type=type_hints["abuse_notification_email"])
            check_type(argname="argument admin_mode", value=admin_mode, expected_type=type_hints["admin_mode"])
            check_type(argname="argument after_sign_out_path", value=after_sign_out_path, expected_type=type_hints["after_sign_out_path"])
            check_type(argname="argument after_sign_up_text", value=after_sign_up_text, expected_type=type_hints["after_sign_up_text"])
            check_type(argname="argument akismet_api_key", value=akismet_api_key, expected_type=type_hints["akismet_api_key"])
            check_type(argname="argument akismet_enabled", value=akismet_enabled, expected_type=type_hints["akismet_enabled"])
            check_type(argname="argument allow_group_owners_to_manage_ldap", value=allow_group_owners_to_manage_ldap, expected_type=type_hints["allow_group_owners_to_manage_ldap"])
            check_type(argname="argument allow_local_requests_from_system_hooks", value=allow_local_requests_from_system_hooks, expected_type=type_hints["allow_local_requests_from_system_hooks"])
            check_type(argname="argument allow_local_requests_from_web_hooks_and_services", value=allow_local_requests_from_web_hooks_and_services, expected_type=type_hints["allow_local_requests_from_web_hooks_and_services"])
            check_type(argname="argument archive_builds_in_human_readable", value=archive_builds_in_human_readable, expected_type=type_hints["archive_builds_in_human_readable"])
            check_type(argname="argument asset_proxy_allowlist", value=asset_proxy_allowlist, expected_type=type_hints["asset_proxy_allowlist"])
            check_type(argname="argument asset_proxy_enabled", value=asset_proxy_enabled, expected_type=type_hints["asset_proxy_enabled"])
            check_type(argname="argument asset_proxy_secret_key", value=asset_proxy_secret_key, expected_type=type_hints["asset_proxy_secret_key"])
            check_type(argname="argument asset_proxy_url", value=asset_proxy_url, expected_type=type_hints["asset_proxy_url"])
            check_type(argname="argument authorized_keys_enabled", value=authorized_keys_enabled, expected_type=type_hints["authorized_keys_enabled"])
            check_type(argname="argument auto_devops_domain", value=auto_devops_domain, expected_type=type_hints["auto_devops_domain"])
            check_type(argname="argument auto_devops_enabled", value=auto_devops_enabled, expected_type=type_hints["auto_devops_enabled"])
            check_type(argname="argument automatic_purchased_storage_allocation", value=automatic_purchased_storage_allocation, expected_type=type_hints["automatic_purchased_storage_allocation"])
            check_type(argname="argument can_create_group", value=can_create_group, expected_type=type_hints["can_create_group"])
            check_type(argname="argument check_namespace_plan", value=check_namespace_plan, expected_type=type_hints["check_namespace_plan"])
            check_type(argname="argument commit_email_hostname", value=commit_email_hostname, expected_type=type_hints["commit_email_hostname"])
            check_type(argname="argument container_expiration_policies_enable_historic_entries", value=container_expiration_policies_enable_historic_entries, expected_type=type_hints["container_expiration_policies_enable_historic_entries"])
            check_type(argname="argument container_registry_cleanup_tags_service_max_list_size", value=container_registry_cleanup_tags_service_max_list_size, expected_type=type_hints["container_registry_cleanup_tags_service_max_list_size"])
            check_type(argname="argument container_registry_delete_tags_service_timeout", value=container_registry_delete_tags_service_timeout, expected_type=type_hints["container_registry_delete_tags_service_timeout"])
            check_type(argname="argument container_registry_expiration_policies_caching", value=container_registry_expiration_policies_caching, expected_type=type_hints["container_registry_expiration_policies_caching"])
            check_type(argname="argument container_registry_expiration_policies_worker_capacity", value=container_registry_expiration_policies_worker_capacity, expected_type=type_hints["container_registry_expiration_policies_worker_capacity"])
            check_type(argname="argument container_registry_token_expire_delay", value=container_registry_token_expire_delay, expected_type=type_hints["container_registry_token_expire_delay"])
            check_type(argname="argument deactivate_dormant_users", value=deactivate_dormant_users, expected_type=type_hints["deactivate_dormant_users"])
            check_type(argname="argument default_artifacts_expire_in", value=default_artifacts_expire_in, expected_type=type_hints["default_artifacts_expire_in"])
            check_type(argname="argument default_branch_name", value=default_branch_name, expected_type=type_hints["default_branch_name"])
            check_type(argname="argument default_branch_protection", value=default_branch_protection, expected_type=type_hints["default_branch_protection"])
            check_type(argname="argument default_ci_config_path", value=default_ci_config_path, expected_type=type_hints["default_ci_config_path"])
            check_type(argname="argument default_group_visibility", value=default_group_visibility, expected_type=type_hints["default_group_visibility"])
            check_type(argname="argument default_project_creation", value=default_project_creation, expected_type=type_hints["default_project_creation"])
            check_type(argname="argument default_projects_limit", value=default_projects_limit, expected_type=type_hints["default_projects_limit"])
            check_type(argname="argument default_project_visibility", value=default_project_visibility, expected_type=type_hints["default_project_visibility"])
            check_type(argname="argument default_snippet_visibility", value=default_snippet_visibility, expected_type=type_hints["default_snippet_visibility"])
            check_type(argname="argument delayed_group_deletion", value=delayed_group_deletion, expected_type=type_hints["delayed_group_deletion"])
            check_type(argname="argument delayed_project_deletion", value=delayed_project_deletion, expected_type=type_hints["delayed_project_deletion"])
            check_type(argname="argument delete_inactive_projects", value=delete_inactive_projects, expected_type=type_hints["delete_inactive_projects"])
            check_type(argname="argument deletion_adjourned_period", value=deletion_adjourned_period, expected_type=type_hints["deletion_adjourned_period"])
            check_type(argname="argument diff_max_files", value=diff_max_files, expected_type=type_hints["diff_max_files"])
            check_type(argname="argument diff_max_lines", value=diff_max_lines, expected_type=type_hints["diff_max_lines"])
            check_type(argname="argument diff_max_patch_bytes", value=diff_max_patch_bytes, expected_type=type_hints["diff_max_patch_bytes"])
            check_type(argname="argument disabled_oauth_sign_in_sources", value=disabled_oauth_sign_in_sources, expected_type=type_hints["disabled_oauth_sign_in_sources"])
            check_type(argname="argument disable_feed_token", value=disable_feed_token, expected_type=type_hints["disable_feed_token"])
            check_type(argname="argument dns_rebinding_protection_enabled", value=dns_rebinding_protection_enabled, expected_type=type_hints["dns_rebinding_protection_enabled"])
            check_type(argname="argument domain_allowlist", value=domain_allowlist, expected_type=type_hints["domain_allowlist"])
            check_type(argname="argument domain_denylist", value=domain_denylist, expected_type=type_hints["domain_denylist"])
            check_type(argname="argument domain_denylist_enabled", value=domain_denylist_enabled, expected_type=type_hints["domain_denylist_enabled"])
            check_type(argname="argument dsa_key_restriction", value=dsa_key_restriction, expected_type=type_hints["dsa_key_restriction"])
            check_type(argname="argument ecdsa_key_restriction", value=ecdsa_key_restriction, expected_type=type_hints["ecdsa_key_restriction"])
            check_type(argname="argument ecdsa_sk_key_restriction", value=ecdsa_sk_key_restriction, expected_type=type_hints["ecdsa_sk_key_restriction"])
            check_type(argname="argument ed25519_key_restriction", value=ed25519_key_restriction, expected_type=type_hints["ed25519_key_restriction"])
            check_type(argname="argument ed25519_sk_key_restriction", value=ed25519_sk_key_restriction, expected_type=type_hints["ed25519_sk_key_restriction"])
            check_type(argname="argument eks_access_key_id", value=eks_access_key_id, expected_type=type_hints["eks_access_key_id"])
            check_type(argname="argument eks_account_id", value=eks_account_id, expected_type=type_hints["eks_account_id"])
            check_type(argname="argument eks_integration_enabled", value=eks_integration_enabled, expected_type=type_hints["eks_integration_enabled"])
            check_type(argname="argument eks_secret_access_key", value=eks_secret_access_key, expected_type=type_hints["eks_secret_access_key"])
            check_type(argname="argument elasticsearch_aws", value=elasticsearch_aws, expected_type=type_hints["elasticsearch_aws"])
            check_type(argname="argument elasticsearch_aws_access_key", value=elasticsearch_aws_access_key, expected_type=type_hints["elasticsearch_aws_access_key"])
            check_type(argname="argument elasticsearch_aws_region", value=elasticsearch_aws_region, expected_type=type_hints["elasticsearch_aws_region"])
            check_type(argname="argument elasticsearch_aws_secret_access_key", value=elasticsearch_aws_secret_access_key, expected_type=type_hints["elasticsearch_aws_secret_access_key"])
            check_type(argname="argument elasticsearch_indexed_field_length_limit", value=elasticsearch_indexed_field_length_limit, expected_type=type_hints["elasticsearch_indexed_field_length_limit"])
            check_type(argname="argument elasticsearch_indexed_file_size_limit_kb", value=elasticsearch_indexed_file_size_limit_kb, expected_type=type_hints["elasticsearch_indexed_file_size_limit_kb"])
            check_type(argname="argument elasticsearch_indexing", value=elasticsearch_indexing, expected_type=type_hints["elasticsearch_indexing"])
            check_type(argname="argument elasticsearch_limit_indexing", value=elasticsearch_limit_indexing, expected_type=type_hints["elasticsearch_limit_indexing"])
            check_type(argname="argument elasticsearch_max_bulk_concurrency", value=elasticsearch_max_bulk_concurrency, expected_type=type_hints["elasticsearch_max_bulk_concurrency"])
            check_type(argname="argument elasticsearch_max_bulk_size_mb", value=elasticsearch_max_bulk_size_mb, expected_type=type_hints["elasticsearch_max_bulk_size_mb"])
            check_type(argname="argument elasticsearch_namespace_ids", value=elasticsearch_namespace_ids, expected_type=type_hints["elasticsearch_namespace_ids"])
            check_type(argname="argument elasticsearch_password", value=elasticsearch_password, expected_type=type_hints["elasticsearch_password"])
            check_type(argname="argument elasticsearch_project_ids", value=elasticsearch_project_ids, expected_type=type_hints["elasticsearch_project_ids"])
            check_type(argname="argument elasticsearch_search", value=elasticsearch_search, expected_type=type_hints["elasticsearch_search"])
            check_type(argname="argument elasticsearch_url", value=elasticsearch_url, expected_type=type_hints["elasticsearch_url"])
            check_type(argname="argument elasticsearch_username", value=elasticsearch_username, expected_type=type_hints["elasticsearch_username"])
            check_type(argname="argument email_additional_text", value=email_additional_text, expected_type=type_hints["email_additional_text"])
            check_type(argname="argument email_author_in_body", value=email_author_in_body, expected_type=type_hints["email_author_in_body"])
            check_type(argname="argument enabled_git_access_protocol", value=enabled_git_access_protocol, expected_type=type_hints["enabled_git_access_protocol"])
            check_type(argname="argument enforce_namespace_storage_limit", value=enforce_namespace_storage_limit, expected_type=type_hints["enforce_namespace_storage_limit"])
            check_type(argname="argument enforce_terms", value=enforce_terms, expected_type=type_hints["enforce_terms"])
            check_type(argname="argument external_auth_client_cert", value=external_auth_client_cert, expected_type=type_hints["external_auth_client_cert"])
            check_type(argname="argument external_auth_client_key", value=external_auth_client_key, expected_type=type_hints["external_auth_client_key"])
            check_type(argname="argument external_auth_client_key_pass", value=external_auth_client_key_pass, expected_type=type_hints["external_auth_client_key_pass"])
            check_type(argname="argument external_authorization_service_default_label", value=external_authorization_service_default_label, expected_type=type_hints["external_authorization_service_default_label"])
            check_type(argname="argument external_authorization_service_enabled", value=external_authorization_service_enabled, expected_type=type_hints["external_authorization_service_enabled"])
            check_type(argname="argument external_authorization_service_timeout", value=external_authorization_service_timeout, expected_type=type_hints["external_authorization_service_timeout"])
            check_type(argname="argument external_authorization_service_url", value=external_authorization_service_url, expected_type=type_hints["external_authorization_service_url"])
            check_type(argname="argument external_pipeline_validation_service_timeout", value=external_pipeline_validation_service_timeout, expected_type=type_hints["external_pipeline_validation_service_timeout"])
            check_type(argname="argument external_pipeline_validation_service_token", value=external_pipeline_validation_service_token, expected_type=type_hints["external_pipeline_validation_service_token"])
            check_type(argname="argument external_pipeline_validation_service_url", value=external_pipeline_validation_service_url, expected_type=type_hints["external_pipeline_validation_service_url"])
            check_type(argname="argument file_template_project_id", value=file_template_project_id, expected_type=type_hints["file_template_project_id"])
            check_type(argname="argument first_day_of_week", value=first_day_of_week, expected_type=type_hints["first_day_of_week"])
            check_type(argname="argument geo_node_allowed_ips", value=geo_node_allowed_ips, expected_type=type_hints["geo_node_allowed_ips"])
            check_type(argname="argument geo_status_timeout", value=geo_status_timeout, expected_type=type_hints["geo_status_timeout"])
            check_type(argname="argument gitaly_timeout_default", value=gitaly_timeout_default, expected_type=type_hints["gitaly_timeout_default"])
            check_type(argname="argument gitaly_timeout_fast", value=gitaly_timeout_fast, expected_type=type_hints["gitaly_timeout_fast"])
            check_type(argname="argument gitaly_timeout_medium", value=gitaly_timeout_medium, expected_type=type_hints["gitaly_timeout_medium"])
            check_type(argname="argument git_rate_limit_users_allowlist", value=git_rate_limit_users_allowlist, expected_type=type_hints["git_rate_limit_users_allowlist"])
            check_type(argname="argument git_two_factor_session_expiry", value=git_two_factor_session_expiry, expected_type=type_hints["git_two_factor_session_expiry"])
            check_type(argname="argument grafana_enabled", value=grafana_enabled, expected_type=type_hints["grafana_enabled"])
            check_type(argname="argument grafana_url", value=grafana_url, expected_type=type_hints["grafana_url"])
            check_type(argname="argument gravatar_enabled", value=gravatar_enabled, expected_type=type_hints["gravatar_enabled"])
            check_type(argname="argument group_owners_can_manage_default_branch_protection", value=group_owners_can_manage_default_branch_protection, expected_type=type_hints["group_owners_can_manage_default_branch_protection"])
            check_type(argname="argument hashed_storage_enabled", value=hashed_storage_enabled, expected_type=type_hints["hashed_storage_enabled"])
            check_type(argname="argument help_page_hide_commercial_content", value=help_page_hide_commercial_content, expected_type=type_hints["help_page_hide_commercial_content"])
            check_type(argname="argument help_page_support_url", value=help_page_support_url, expected_type=type_hints["help_page_support_url"])
            check_type(argname="argument help_page_text", value=help_page_text, expected_type=type_hints["help_page_text"])
            check_type(argname="argument help_text", value=help_text, expected_type=type_hints["help_text"])
            check_type(argname="argument hide_third_party_offers", value=hide_third_party_offers, expected_type=type_hints["hide_third_party_offers"])
            check_type(argname="argument home_page_url", value=home_page_url, expected_type=type_hints["home_page_url"])
            check_type(argname="argument housekeeping_enabled", value=housekeeping_enabled, expected_type=type_hints["housekeeping_enabled"])
            check_type(argname="argument housekeeping_full_repack_period", value=housekeeping_full_repack_period, expected_type=type_hints["housekeeping_full_repack_period"])
            check_type(argname="argument housekeeping_gc_period", value=housekeeping_gc_period, expected_type=type_hints["housekeeping_gc_period"])
            check_type(argname="argument housekeeping_incremental_repack_period", value=housekeeping_incremental_repack_period, expected_type=type_hints["housekeeping_incremental_repack_period"])
            check_type(argname="argument html_emails_enabled", value=html_emails_enabled, expected_type=type_hints["html_emails_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument import_sources", value=import_sources, expected_type=type_hints["import_sources"])
            check_type(argname="argument inactive_projects_delete_after_months", value=inactive_projects_delete_after_months, expected_type=type_hints["inactive_projects_delete_after_months"])
            check_type(argname="argument inactive_projects_min_size_mb", value=inactive_projects_min_size_mb, expected_type=type_hints["inactive_projects_min_size_mb"])
            check_type(argname="argument inactive_projects_send_warning_email_after_months", value=inactive_projects_send_warning_email_after_months, expected_type=type_hints["inactive_projects_send_warning_email_after_months"])
            check_type(argname="argument in_product_marketing_emails_enabled", value=in_product_marketing_emails_enabled, expected_type=type_hints["in_product_marketing_emails_enabled"])
            check_type(argname="argument invisible_captcha_enabled", value=invisible_captcha_enabled, expected_type=type_hints["invisible_captcha_enabled"])
            check_type(argname="argument issues_create_limit", value=issues_create_limit, expected_type=type_hints["issues_create_limit"])
            check_type(argname="argument keep_latest_artifact", value=keep_latest_artifact, expected_type=type_hints["keep_latest_artifact"])
            check_type(argname="argument local_markdown_version", value=local_markdown_version, expected_type=type_hints["local_markdown_version"])
            check_type(argname="argument mailgun_events_enabled", value=mailgun_events_enabled, expected_type=type_hints["mailgun_events_enabled"])
            check_type(argname="argument mailgun_signing_key", value=mailgun_signing_key, expected_type=type_hints["mailgun_signing_key"])
            check_type(argname="argument maintenance_mode", value=maintenance_mode, expected_type=type_hints["maintenance_mode"])
            check_type(argname="argument maintenance_mode_message", value=maintenance_mode_message, expected_type=type_hints["maintenance_mode_message"])
            check_type(argname="argument max_artifacts_size", value=max_artifacts_size, expected_type=type_hints["max_artifacts_size"])
            check_type(argname="argument max_attachment_size", value=max_attachment_size, expected_type=type_hints["max_attachment_size"])
            check_type(argname="argument max_export_size", value=max_export_size, expected_type=type_hints["max_export_size"])
            check_type(argname="argument max_import_size", value=max_import_size, expected_type=type_hints["max_import_size"])
            check_type(argname="argument max_number_of_repository_downloads", value=max_number_of_repository_downloads, expected_type=type_hints["max_number_of_repository_downloads"])
            check_type(argname="argument max_number_of_repository_downloads_within_time_period", value=max_number_of_repository_downloads_within_time_period, expected_type=type_hints["max_number_of_repository_downloads_within_time_period"])
            check_type(argname="argument max_pages_size", value=max_pages_size, expected_type=type_hints["max_pages_size"])
            check_type(argname="argument max_personal_access_token_lifetime", value=max_personal_access_token_lifetime, expected_type=type_hints["max_personal_access_token_lifetime"])
            check_type(argname="argument max_ssh_key_lifetime", value=max_ssh_key_lifetime, expected_type=type_hints["max_ssh_key_lifetime"])
            check_type(argname="argument metrics_method_call_threshold", value=metrics_method_call_threshold, expected_type=type_hints["metrics_method_call_threshold"])
            check_type(argname="argument mirror_available", value=mirror_available, expected_type=type_hints["mirror_available"])
            check_type(argname="argument mirror_capacity_threshold", value=mirror_capacity_threshold, expected_type=type_hints["mirror_capacity_threshold"])
            check_type(argname="argument mirror_max_capacity", value=mirror_max_capacity, expected_type=type_hints["mirror_max_capacity"])
            check_type(argname="argument mirror_max_delay", value=mirror_max_delay, expected_type=type_hints["mirror_max_delay"])
            check_type(argname="argument npm_package_requests_forwarding", value=npm_package_requests_forwarding, expected_type=type_hints["npm_package_requests_forwarding"])
            check_type(argname="argument outbound_local_requests_whitelist", value=outbound_local_requests_whitelist, expected_type=type_hints["outbound_local_requests_whitelist"])
            check_type(argname="argument package_registry_cleanup_policies_worker_capacity", value=package_registry_cleanup_policies_worker_capacity, expected_type=type_hints["package_registry_cleanup_policies_worker_capacity"])
            check_type(argname="argument pages_domain_verification_enabled", value=pages_domain_verification_enabled, expected_type=type_hints["pages_domain_verification_enabled"])
            check_type(argname="argument password_authentication_enabled_for_git", value=password_authentication_enabled_for_git, expected_type=type_hints["password_authentication_enabled_for_git"])
            check_type(argname="argument password_authentication_enabled_for_web", value=password_authentication_enabled_for_web, expected_type=type_hints["password_authentication_enabled_for_web"])
            check_type(argname="argument password_lowercase_required", value=password_lowercase_required, expected_type=type_hints["password_lowercase_required"])
            check_type(argname="argument password_number_required", value=password_number_required, expected_type=type_hints["password_number_required"])
            check_type(argname="argument password_symbol_required", value=password_symbol_required, expected_type=type_hints["password_symbol_required"])
            check_type(argname="argument password_uppercase_required", value=password_uppercase_required, expected_type=type_hints["password_uppercase_required"])
            check_type(argname="argument performance_bar_allowed_group_path", value=performance_bar_allowed_group_path, expected_type=type_hints["performance_bar_allowed_group_path"])
            check_type(argname="argument personal_access_token_prefix", value=personal_access_token_prefix, expected_type=type_hints["personal_access_token_prefix"])
            check_type(argname="argument pipeline_limit_per_project_user_sha", value=pipeline_limit_per_project_user_sha, expected_type=type_hints["pipeline_limit_per_project_user_sha"])
            check_type(argname="argument plantuml_enabled", value=plantuml_enabled, expected_type=type_hints["plantuml_enabled"])
            check_type(argname="argument plantuml_url", value=plantuml_url, expected_type=type_hints["plantuml_url"])
            check_type(argname="argument polling_interval_multiplier", value=polling_interval_multiplier, expected_type=type_hints["polling_interval_multiplier"])
            check_type(argname="argument project_export_enabled", value=project_export_enabled, expected_type=type_hints["project_export_enabled"])
            check_type(argname="argument prometheus_metrics_enabled", value=prometheus_metrics_enabled, expected_type=type_hints["prometheus_metrics_enabled"])
            check_type(argname="argument protected_ci_variables", value=protected_ci_variables, expected_type=type_hints["protected_ci_variables"])
            check_type(argname="argument push_event_activities_limit", value=push_event_activities_limit, expected_type=type_hints["push_event_activities_limit"])
            check_type(argname="argument push_event_hooks_limit", value=push_event_hooks_limit, expected_type=type_hints["push_event_hooks_limit"])
            check_type(argname="argument pypi_package_requests_forwarding", value=pypi_package_requests_forwarding, expected_type=type_hints["pypi_package_requests_forwarding"])
            check_type(argname="argument rate_limiting_response_text", value=rate_limiting_response_text, expected_type=type_hints["rate_limiting_response_text"])
            check_type(argname="argument raw_blob_request_limit", value=raw_blob_request_limit, expected_type=type_hints["raw_blob_request_limit"])
            check_type(argname="argument recaptcha_enabled", value=recaptcha_enabled, expected_type=type_hints["recaptcha_enabled"])
            check_type(argname="argument recaptcha_private_key", value=recaptcha_private_key, expected_type=type_hints["recaptcha_private_key"])
            check_type(argname="argument recaptcha_site_key", value=recaptcha_site_key, expected_type=type_hints["recaptcha_site_key"])
            check_type(argname="argument receive_max_input_size", value=receive_max_input_size, expected_type=type_hints["receive_max_input_size"])
            check_type(argname="argument repository_checks_enabled", value=repository_checks_enabled, expected_type=type_hints["repository_checks_enabled"])
            check_type(argname="argument repository_size_limit", value=repository_size_limit, expected_type=type_hints["repository_size_limit"])
            check_type(argname="argument repository_storages", value=repository_storages, expected_type=type_hints["repository_storages"])
            check_type(argname="argument repository_storages_weighted", value=repository_storages_weighted, expected_type=type_hints["repository_storages_weighted"])
            check_type(argname="argument require_admin_approval_after_user_signup", value=require_admin_approval_after_user_signup, expected_type=type_hints["require_admin_approval_after_user_signup"])
            check_type(argname="argument require_two_factor_authentication", value=require_two_factor_authentication, expected_type=type_hints["require_two_factor_authentication"])
            check_type(argname="argument restricted_visibility_levels", value=restricted_visibility_levels, expected_type=type_hints["restricted_visibility_levels"])
            check_type(argname="argument rsa_key_restriction", value=rsa_key_restriction, expected_type=type_hints["rsa_key_restriction"])
            check_type(argname="argument search_rate_limit", value=search_rate_limit, expected_type=type_hints["search_rate_limit"])
            check_type(argname="argument search_rate_limit_unauthenticated", value=search_rate_limit_unauthenticated, expected_type=type_hints["search_rate_limit_unauthenticated"])
            check_type(argname="argument send_user_confirmation_email", value=send_user_confirmation_email, expected_type=type_hints["send_user_confirmation_email"])
            check_type(argname="argument session_expire_delay", value=session_expire_delay, expected_type=type_hints["session_expire_delay"])
            check_type(argname="argument shared_runners_enabled", value=shared_runners_enabled, expected_type=type_hints["shared_runners_enabled"])
            check_type(argname="argument shared_runners_minutes", value=shared_runners_minutes, expected_type=type_hints["shared_runners_minutes"])
            check_type(argname="argument shared_runners_text", value=shared_runners_text, expected_type=type_hints["shared_runners_text"])
            check_type(argname="argument sidekiq_job_limiter_compression_threshold_bytes", value=sidekiq_job_limiter_compression_threshold_bytes, expected_type=type_hints["sidekiq_job_limiter_compression_threshold_bytes"])
            check_type(argname="argument sidekiq_job_limiter_limit_bytes", value=sidekiq_job_limiter_limit_bytes, expected_type=type_hints["sidekiq_job_limiter_limit_bytes"])
            check_type(argname="argument sidekiq_job_limiter_mode", value=sidekiq_job_limiter_mode, expected_type=type_hints["sidekiq_job_limiter_mode"])
            check_type(argname="argument sign_in_text", value=sign_in_text, expected_type=type_hints["sign_in_text"])
            check_type(argname="argument signup_enabled", value=signup_enabled, expected_type=type_hints["signup_enabled"])
            check_type(argname="argument slack_app_enabled", value=slack_app_enabled, expected_type=type_hints["slack_app_enabled"])
            check_type(argname="argument slack_app_id", value=slack_app_id, expected_type=type_hints["slack_app_id"])
            check_type(argname="argument slack_app_secret", value=slack_app_secret, expected_type=type_hints["slack_app_secret"])
            check_type(argname="argument slack_app_signing_secret", value=slack_app_signing_secret, expected_type=type_hints["slack_app_signing_secret"])
            check_type(argname="argument slack_app_verification_token", value=slack_app_verification_token, expected_type=type_hints["slack_app_verification_token"])
            check_type(argname="argument snippet_size_limit", value=snippet_size_limit, expected_type=type_hints["snippet_size_limit"])
            check_type(argname="argument snowplow_app_id", value=snowplow_app_id, expected_type=type_hints["snowplow_app_id"])
            check_type(argname="argument snowplow_collector_hostname", value=snowplow_collector_hostname, expected_type=type_hints["snowplow_collector_hostname"])
            check_type(argname="argument snowplow_cookie_domain", value=snowplow_cookie_domain, expected_type=type_hints["snowplow_cookie_domain"])
            check_type(argname="argument snowplow_enabled", value=snowplow_enabled, expected_type=type_hints["snowplow_enabled"])
            check_type(argname="argument sourcegraph_enabled", value=sourcegraph_enabled, expected_type=type_hints["sourcegraph_enabled"])
            check_type(argname="argument sourcegraph_public_only", value=sourcegraph_public_only, expected_type=type_hints["sourcegraph_public_only"])
            check_type(argname="argument sourcegraph_url", value=sourcegraph_url, expected_type=type_hints["sourcegraph_url"])
            check_type(argname="argument spam_check_api_key", value=spam_check_api_key, expected_type=type_hints["spam_check_api_key"])
            check_type(argname="argument spam_check_endpoint_enabled", value=spam_check_endpoint_enabled, expected_type=type_hints["spam_check_endpoint_enabled"])
            check_type(argname="argument spam_check_endpoint_url", value=spam_check_endpoint_url, expected_type=type_hints["spam_check_endpoint_url"])
            check_type(argname="argument suggest_pipeline_enabled", value=suggest_pipeline_enabled, expected_type=type_hints["suggest_pipeline_enabled"])
            check_type(argname="argument terminal_max_session_time", value=terminal_max_session_time, expected_type=type_hints["terminal_max_session_time"])
            check_type(argname="argument terms", value=terms, expected_type=type_hints["terms"])
            check_type(argname="argument throttle_authenticated_api_enabled", value=throttle_authenticated_api_enabled, expected_type=type_hints["throttle_authenticated_api_enabled"])
            check_type(argname="argument throttle_authenticated_api_period_in_seconds", value=throttle_authenticated_api_period_in_seconds, expected_type=type_hints["throttle_authenticated_api_period_in_seconds"])
            check_type(argname="argument throttle_authenticated_api_requests_per_period", value=throttle_authenticated_api_requests_per_period, expected_type=type_hints["throttle_authenticated_api_requests_per_period"])
            check_type(argname="argument throttle_authenticated_packages_api_enabled", value=throttle_authenticated_packages_api_enabled, expected_type=type_hints["throttle_authenticated_packages_api_enabled"])
            check_type(argname="argument throttle_authenticated_packages_api_period_in_seconds", value=throttle_authenticated_packages_api_period_in_seconds, expected_type=type_hints["throttle_authenticated_packages_api_period_in_seconds"])
            check_type(argname="argument throttle_authenticated_packages_api_requests_per_period", value=throttle_authenticated_packages_api_requests_per_period, expected_type=type_hints["throttle_authenticated_packages_api_requests_per_period"])
            check_type(argname="argument throttle_authenticated_web_enabled", value=throttle_authenticated_web_enabled, expected_type=type_hints["throttle_authenticated_web_enabled"])
            check_type(argname="argument throttle_authenticated_web_period_in_seconds", value=throttle_authenticated_web_period_in_seconds, expected_type=type_hints["throttle_authenticated_web_period_in_seconds"])
            check_type(argname="argument throttle_authenticated_web_requests_per_period", value=throttle_authenticated_web_requests_per_period, expected_type=type_hints["throttle_authenticated_web_requests_per_period"])
            check_type(argname="argument throttle_unauthenticated_api_enabled", value=throttle_unauthenticated_api_enabled, expected_type=type_hints["throttle_unauthenticated_api_enabled"])
            check_type(argname="argument throttle_unauthenticated_api_period_in_seconds", value=throttle_unauthenticated_api_period_in_seconds, expected_type=type_hints["throttle_unauthenticated_api_period_in_seconds"])
            check_type(argname="argument throttle_unauthenticated_api_requests_per_period", value=throttle_unauthenticated_api_requests_per_period, expected_type=type_hints["throttle_unauthenticated_api_requests_per_period"])
            check_type(argname="argument throttle_unauthenticated_packages_api_enabled", value=throttle_unauthenticated_packages_api_enabled, expected_type=type_hints["throttle_unauthenticated_packages_api_enabled"])
            check_type(argname="argument throttle_unauthenticated_packages_api_period_in_seconds", value=throttle_unauthenticated_packages_api_period_in_seconds, expected_type=type_hints["throttle_unauthenticated_packages_api_period_in_seconds"])
            check_type(argname="argument throttle_unauthenticated_packages_api_requests_per_period", value=throttle_unauthenticated_packages_api_requests_per_period, expected_type=type_hints["throttle_unauthenticated_packages_api_requests_per_period"])
            check_type(argname="argument throttle_unauthenticated_web_enabled", value=throttle_unauthenticated_web_enabled, expected_type=type_hints["throttle_unauthenticated_web_enabled"])
            check_type(argname="argument throttle_unauthenticated_web_period_in_seconds", value=throttle_unauthenticated_web_period_in_seconds, expected_type=type_hints["throttle_unauthenticated_web_period_in_seconds"])
            check_type(argname="argument throttle_unauthenticated_web_requests_per_period", value=throttle_unauthenticated_web_requests_per_period, expected_type=type_hints["throttle_unauthenticated_web_requests_per_period"])
            check_type(argname="argument time_tracking_limit_to_hours", value=time_tracking_limit_to_hours, expected_type=type_hints["time_tracking_limit_to_hours"])
            check_type(argname="argument two_factor_grace_period", value=two_factor_grace_period, expected_type=type_hints["two_factor_grace_period"])
            check_type(argname="argument unique_ips_limit_enabled", value=unique_ips_limit_enabled, expected_type=type_hints["unique_ips_limit_enabled"])
            check_type(argname="argument unique_ips_limit_per_user", value=unique_ips_limit_per_user, expected_type=type_hints["unique_ips_limit_per_user"])
            check_type(argname="argument unique_ips_limit_time_window", value=unique_ips_limit_time_window, expected_type=type_hints["unique_ips_limit_time_window"])
            check_type(argname="argument usage_ping_enabled", value=usage_ping_enabled, expected_type=type_hints["usage_ping_enabled"])
            check_type(argname="argument user_deactivation_emails_enabled", value=user_deactivation_emails_enabled, expected_type=type_hints["user_deactivation_emails_enabled"])
            check_type(argname="argument user_default_external", value=user_default_external, expected_type=type_hints["user_default_external"])
            check_type(argname="argument user_default_internal_regex", value=user_default_internal_regex, expected_type=type_hints["user_default_internal_regex"])
            check_type(argname="argument user_oauth_applications", value=user_oauth_applications, expected_type=type_hints["user_oauth_applications"])
            check_type(argname="argument user_show_add_ssh_key_message", value=user_show_add_ssh_key_message, expected_type=type_hints["user_show_add_ssh_key_message"])
            check_type(argname="argument version_check_enabled", value=version_check_enabled, expected_type=type_hints["version_check_enabled"])
            check_type(argname="argument web_ide_clientside_preview_enabled", value=web_ide_clientside_preview_enabled, expected_type=type_hints["web_ide_clientside_preview_enabled"])
            check_type(argname="argument whats_new_variant", value=whats_new_variant, expected_type=type_hints["whats_new_variant"])
            check_type(argname="argument wiki_page_max_content_bytes", value=wiki_page_max_content_bytes, expected_type=type_hints["wiki_page_max_content_bytes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if abuse_notification_email is not None:
            self._values["abuse_notification_email"] = abuse_notification_email
        if admin_mode is not None:
            self._values["admin_mode"] = admin_mode
        if after_sign_out_path is not None:
            self._values["after_sign_out_path"] = after_sign_out_path
        if after_sign_up_text is not None:
            self._values["after_sign_up_text"] = after_sign_up_text
        if akismet_api_key is not None:
            self._values["akismet_api_key"] = akismet_api_key
        if akismet_enabled is not None:
            self._values["akismet_enabled"] = akismet_enabled
        if allow_group_owners_to_manage_ldap is not None:
            self._values["allow_group_owners_to_manage_ldap"] = allow_group_owners_to_manage_ldap
        if allow_local_requests_from_system_hooks is not None:
            self._values["allow_local_requests_from_system_hooks"] = allow_local_requests_from_system_hooks
        if allow_local_requests_from_web_hooks_and_services is not None:
            self._values["allow_local_requests_from_web_hooks_and_services"] = allow_local_requests_from_web_hooks_and_services
        if archive_builds_in_human_readable is not None:
            self._values["archive_builds_in_human_readable"] = archive_builds_in_human_readable
        if asset_proxy_allowlist is not None:
            self._values["asset_proxy_allowlist"] = asset_proxy_allowlist
        if asset_proxy_enabled is not None:
            self._values["asset_proxy_enabled"] = asset_proxy_enabled
        if asset_proxy_secret_key is not None:
            self._values["asset_proxy_secret_key"] = asset_proxy_secret_key
        if asset_proxy_url is not None:
            self._values["asset_proxy_url"] = asset_proxy_url
        if authorized_keys_enabled is not None:
            self._values["authorized_keys_enabled"] = authorized_keys_enabled
        if auto_devops_domain is not None:
            self._values["auto_devops_domain"] = auto_devops_domain
        if auto_devops_enabled is not None:
            self._values["auto_devops_enabled"] = auto_devops_enabled
        if automatic_purchased_storage_allocation is not None:
            self._values["automatic_purchased_storage_allocation"] = automatic_purchased_storage_allocation
        if can_create_group is not None:
            self._values["can_create_group"] = can_create_group
        if check_namespace_plan is not None:
            self._values["check_namespace_plan"] = check_namespace_plan
        if commit_email_hostname is not None:
            self._values["commit_email_hostname"] = commit_email_hostname
        if container_expiration_policies_enable_historic_entries is not None:
            self._values["container_expiration_policies_enable_historic_entries"] = container_expiration_policies_enable_historic_entries
        if container_registry_cleanup_tags_service_max_list_size is not None:
            self._values["container_registry_cleanup_tags_service_max_list_size"] = container_registry_cleanup_tags_service_max_list_size
        if container_registry_delete_tags_service_timeout is not None:
            self._values["container_registry_delete_tags_service_timeout"] = container_registry_delete_tags_service_timeout
        if container_registry_expiration_policies_caching is not None:
            self._values["container_registry_expiration_policies_caching"] = container_registry_expiration_policies_caching
        if container_registry_expiration_policies_worker_capacity is not None:
            self._values["container_registry_expiration_policies_worker_capacity"] = container_registry_expiration_policies_worker_capacity
        if container_registry_token_expire_delay is not None:
            self._values["container_registry_token_expire_delay"] = container_registry_token_expire_delay
        if deactivate_dormant_users is not None:
            self._values["deactivate_dormant_users"] = deactivate_dormant_users
        if default_artifacts_expire_in is not None:
            self._values["default_artifacts_expire_in"] = default_artifacts_expire_in
        if default_branch_name is not None:
            self._values["default_branch_name"] = default_branch_name
        if default_branch_protection is not None:
            self._values["default_branch_protection"] = default_branch_protection
        if default_ci_config_path is not None:
            self._values["default_ci_config_path"] = default_ci_config_path
        if default_group_visibility is not None:
            self._values["default_group_visibility"] = default_group_visibility
        if default_project_creation is not None:
            self._values["default_project_creation"] = default_project_creation
        if default_projects_limit is not None:
            self._values["default_projects_limit"] = default_projects_limit
        if default_project_visibility is not None:
            self._values["default_project_visibility"] = default_project_visibility
        if default_snippet_visibility is not None:
            self._values["default_snippet_visibility"] = default_snippet_visibility
        if delayed_group_deletion is not None:
            self._values["delayed_group_deletion"] = delayed_group_deletion
        if delayed_project_deletion is not None:
            self._values["delayed_project_deletion"] = delayed_project_deletion
        if delete_inactive_projects is not None:
            self._values["delete_inactive_projects"] = delete_inactive_projects
        if deletion_adjourned_period is not None:
            self._values["deletion_adjourned_period"] = deletion_adjourned_period
        if diff_max_files is not None:
            self._values["diff_max_files"] = diff_max_files
        if diff_max_lines is not None:
            self._values["diff_max_lines"] = diff_max_lines
        if diff_max_patch_bytes is not None:
            self._values["diff_max_patch_bytes"] = diff_max_patch_bytes
        if disabled_oauth_sign_in_sources is not None:
            self._values["disabled_oauth_sign_in_sources"] = disabled_oauth_sign_in_sources
        if disable_feed_token is not None:
            self._values["disable_feed_token"] = disable_feed_token
        if dns_rebinding_protection_enabled is not None:
            self._values["dns_rebinding_protection_enabled"] = dns_rebinding_protection_enabled
        if domain_allowlist is not None:
            self._values["domain_allowlist"] = domain_allowlist
        if domain_denylist is not None:
            self._values["domain_denylist"] = domain_denylist
        if domain_denylist_enabled is not None:
            self._values["domain_denylist_enabled"] = domain_denylist_enabled
        if dsa_key_restriction is not None:
            self._values["dsa_key_restriction"] = dsa_key_restriction
        if ecdsa_key_restriction is not None:
            self._values["ecdsa_key_restriction"] = ecdsa_key_restriction
        if ecdsa_sk_key_restriction is not None:
            self._values["ecdsa_sk_key_restriction"] = ecdsa_sk_key_restriction
        if ed25519_key_restriction is not None:
            self._values["ed25519_key_restriction"] = ed25519_key_restriction
        if ed25519_sk_key_restriction is not None:
            self._values["ed25519_sk_key_restriction"] = ed25519_sk_key_restriction
        if eks_access_key_id is not None:
            self._values["eks_access_key_id"] = eks_access_key_id
        if eks_account_id is not None:
            self._values["eks_account_id"] = eks_account_id
        if eks_integration_enabled is not None:
            self._values["eks_integration_enabled"] = eks_integration_enabled
        if eks_secret_access_key is not None:
            self._values["eks_secret_access_key"] = eks_secret_access_key
        if elasticsearch_aws is not None:
            self._values["elasticsearch_aws"] = elasticsearch_aws
        if elasticsearch_aws_access_key is not None:
            self._values["elasticsearch_aws_access_key"] = elasticsearch_aws_access_key
        if elasticsearch_aws_region is not None:
            self._values["elasticsearch_aws_region"] = elasticsearch_aws_region
        if elasticsearch_aws_secret_access_key is not None:
            self._values["elasticsearch_aws_secret_access_key"] = elasticsearch_aws_secret_access_key
        if elasticsearch_indexed_field_length_limit is not None:
            self._values["elasticsearch_indexed_field_length_limit"] = elasticsearch_indexed_field_length_limit
        if elasticsearch_indexed_file_size_limit_kb is not None:
            self._values["elasticsearch_indexed_file_size_limit_kb"] = elasticsearch_indexed_file_size_limit_kb
        if elasticsearch_indexing is not None:
            self._values["elasticsearch_indexing"] = elasticsearch_indexing
        if elasticsearch_limit_indexing is not None:
            self._values["elasticsearch_limit_indexing"] = elasticsearch_limit_indexing
        if elasticsearch_max_bulk_concurrency is not None:
            self._values["elasticsearch_max_bulk_concurrency"] = elasticsearch_max_bulk_concurrency
        if elasticsearch_max_bulk_size_mb is not None:
            self._values["elasticsearch_max_bulk_size_mb"] = elasticsearch_max_bulk_size_mb
        if elasticsearch_namespace_ids is not None:
            self._values["elasticsearch_namespace_ids"] = elasticsearch_namespace_ids
        if elasticsearch_password is not None:
            self._values["elasticsearch_password"] = elasticsearch_password
        if elasticsearch_project_ids is not None:
            self._values["elasticsearch_project_ids"] = elasticsearch_project_ids
        if elasticsearch_search is not None:
            self._values["elasticsearch_search"] = elasticsearch_search
        if elasticsearch_url is not None:
            self._values["elasticsearch_url"] = elasticsearch_url
        if elasticsearch_username is not None:
            self._values["elasticsearch_username"] = elasticsearch_username
        if email_additional_text is not None:
            self._values["email_additional_text"] = email_additional_text
        if email_author_in_body is not None:
            self._values["email_author_in_body"] = email_author_in_body
        if enabled_git_access_protocol is not None:
            self._values["enabled_git_access_protocol"] = enabled_git_access_protocol
        if enforce_namespace_storage_limit is not None:
            self._values["enforce_namespace_storage_limit"] = enforce_namespace_storage_limit
        if enforce_terms is not None:
            self._values["enforce_terms"] = enforce_terms
        if external_auth_client_cert is not None:
            self._values["external_auth_client_cert"] = external_auth_client_cert
        if external_auth_client_key is not None:
            self._values["external_auth_client_key"] = external_auth_client_key
        if external_auth_client_key_pass is not None:
            self._values["external_auth_client_key_pass"] = external_auth_client_key_pass
        if external_authorization_service_default_label is not None:
            self._values["external_authorization_service_default_label"] = external_authorization_service_default_label
        if external_authorization_service_enabled is not None:
            self._values["external_authorization_service_enabled"] = external_authorization_service_enabled
        if external_authorization_service_timeout is not None:
            self._values["external_authorization_service_timeout"] = external_authorization_service_timeout
        if external_authorization_service_url is not None:
            self._values["external_authorization_service_url"] = external_authorization_service_url
        if external_pipeline_validation_service_timeout is not None:
            self._values["external_pipeline_validation_service_timeout"] = external_pipeline_validation_service_timeout
        if external_pipeline_validation_service_token is not None:
            self._values["external_pipeline_validation_service_token"] = external_pipeline_validation_service_token
        if external_pipeline_validation_service_url is not None:
            self._values["external_pipeline_validation_service_url"] = external_pipeline_validation_service_url
        if file_template_project_id is not None:
            self._values["file_template_project_id"] = file_template_project_id
        if first_day_of_week is not None:
            self._values["first_day_of_week"] = first_day_of_week
        if geo_node_allowed_ips is not None:
            self._values["geo_node_allowed_ips"] = geo_node_allowed_ips
        if geo_status_timeout is not None:
            self._values["geo_status_timeout"] = geo_status_timeout
        if gitaly_timeout_default is not None:
            self._values["gitaly_timeout_default"] = gitaly_timeout_default
        if gitaly_timeout_fast is not None:
            self._values["gitaly_timeout_fast"] = gitaly_timeout_fast
        if gitaly_timeout_medium is not None:
            self._values["gitaly_timeout_medium"] = gitaly_timeout_medium
        if git_rate_limit_users_allowlist is not None:
            self._values["git_rate_limit_users_allowlist"] = git_rate_limit_users_allowlist
        if git_two_factor_session_expiry is not None:
            self._values["git_two_factor_session_expiry"] = git_two_factor_session_expiry
        if grafana_enabled is not None:
            self._values["grafana_enabled"] = grafana_enabled
        if grafana_url is not None:
            self._values["grafana_url"] = grafana_url
        if gravatar_enabled is not None:
            self._values["gravatar_enabled"] = gravatar_enabled
        if group_owners_can_manage_default_branch_protection is not None:
            self._values["group_owners_can_manage_default_branch_protection"] = group_owners_can_manage_default_branch_protection
        if hashed_storage_enabled is not None:
            self._values["hashed_storage_enabled"] = hashed_storage_enabled
        if help_page_hide_commercial_content is not None:
            self._values["help_page_hide_commercial_content"] = help_page_hide_commercial_content
        if help_page_support_url is not None:
            self._values["help_page_support_url"] = help_page_support_url
        if help_page_text is not None:
            self._values["help_page_text"] = help_page_text
        if help_text is not None:
            self._values["help_text"] = help_text
        if hide_third_party_offers is not None:
            self._values["hide_third_party_offers"] = hide_third_party_offers
        if home_page_url is not None:
            self._values["home_page_url"] = home_page_url
        if housekeeping_enabled is not None:
            self._values["housekeeping_enabled"] = housekeeping_enabled
        if housekeeping_full_repack_period is not None:
            self._values["housekeeping_full_repack_period"] = housekeeping_full_repack_period
        if housekeeping_gc_period is not None:
            self._values["housekeeping_gc_period"] = housekeeping_gc_period
        if housekeeping_incremental_repack_period is not None:
            self._values["housekeeping_incremental_repack_period"] = housekeeping_incremental_repack_period
        if html_emails_enabled is not None:
            self._values["html_emails_enabled"] = html_emails_enabled
        if id is not None:
            self._values["id"] = id
        if import_sources is not None:
            self._values["import_sources"] = import_sources
        if inactive_projects_delete_after_months is not None:
            self._values["inactive_projects_delete_after_months"] = inactive_projects_delete_after_months
        if inactive_projects_min_size_mb is not None:
            self._values["inactive_projects_min_size_mb"] = inactive_projects_min_size_mb
        if inactive_projects_send_warning_email_after_months is not None:
            self._values["inactive_projects_send_warning_email_after_months"] = inactive_projects_send_warning_email_after_months
        if in_product_marketing_emails_enabled is not None:
            self._values["in_product_marketing_emails_enabled"] = in_product_marketing_emails_enabled
        if invisible_captcha_enabled is not None:
            self._values["invisible_captcha_enabled"] = invisible_captcha_enabled
        if issues_create_limit is not None:
            self._values["issues_create_limit"] = issues_create_limit
        if keep_latest_artifact is not None:
            self._values["keep_latest_artifact"] = keep_latest_artifact
        if local_markdown_version is not None:
            self._values["local_markdown_version"] = local_markdown_version
        if mailgun_events_enabled is not None:
            self._values["mailgun_events_enabled"] = mailgun_events_enabled
        if mailgun_signing_key is not None:
            self._values["mailgun_signing_key"] = mailgun_signing_key
        if maintenance_mode is not None:
            self._values["maintenance_mode"] = maintenance_mode
        if maintenance_mode_message is not None:
            self._values["maintenance_mode_message"] = maintenance_mode_message
        if max_artifacts_size is not None:
            self._values["max_artifacts_size"] = max_artifacts_size
        if max_attachment_size is not None:
            self._values["max_attachment_size"] = max_attachment_size
        if max_export_size is not None:
            self._values["max_export_size"] = max_export_size
        if max_import_size is not None:
            self._values["max_import_size"] = max_import_size
        if max_number_of_repository_downloads is not None:
            self._values["max_number_of_repository_downloads"] = max_number_of_repository_downloads
        if max_number_of_repository_downloads_within_time_period is not None:
            self._values["max_number_of_repository_downloads_within_time_period"] = max_number_of_repository_downloads_within_time_period
        if max_pages_size is not None:
            self._values["max_pages_size"] = max_pages_size
        if max_personal_access_token_lifetime is not None:
            self._values["max_personal_access_token_lifetime"] = max_personal_access_token_lifetime
        if max_ssh_key_lifetime is not None:
            self._values["max_ssh_key_lifetime"] = max_ssh_key_lifetime
        if metrics_method_call_threshold is not None:
            self._values["metrics_method_call_threshold"] = metrics_method_call_threshold
        if mirror_available is not None:
            self._values["mirror_available"] = mirror_available
        if mirror_capacity_threshold is not None:
            self._values["mirror_capacity_threshold"] = mirror_capacity_threshold
        if mirror_max_capacity is not None:
            self._values["mirror_max_capacity"] = mirror_max_capacity
        if mirror_max_delay is not None:
            self._values["mirror_max_delay"] = mirror_max_delay
        if npm_package_requests_forwarding is not None:
            self._values["npm_package_requests_forwarding"] = npm_package_requests_forwarding
        if outbound_local_requests_whitelist is not None:
            self._values["outbound_local_requests_whitelist"] = outbound_local_requests_whitelist
        if package_registry_cleanup_policies_worker_capacity is not None:
            self._values["package_registry_cleanup_policies_worker_capacity"] = package_registry_cleanup_policies_worker_capacity
        if pages_domain_verification_enabled is not None:
            self._values["pages_domain_verification_enabled"] = pages_domain_verification_enabled
        if password_authentication_enabled_for_git is not None:
            self._values["password_authentication_enabled_for_git"] = password_authentication_enabled_for_git
        if password_authentication_enabled_for_web is not None:
            self._values["password_authentication_enabled_for_web"] = password_authentication_enabled_for_web
        if password_lowercase_required is not None:
            self._values["password_lowercase_required"] = password_lowercase_required
        if password_number_required is not None:
            self._values["password_number_required"] = password_number_required
        if password_symbol_required is not None:
            self._values["password_symbol_required"] = password_symbol_required
        if password_uppercase_required is not None:
            self._values["password_uppercase_required"] = password_uppercase_required
        if performance_bar_allowed_group_path is not None:
            self._values["performance_bar_allowed_group_path"] = performance_bar_allowed_group_path
        if personal_access_token_prefix is not None:
            self._values["personal_access_token_prefix"] = personal_access_token_prefix
        if pipeline_limit_per_project_user_sha is not None:
            self._values["pipeline_limit_per_project_user_sha"] = pipeline_limit_per_project_user_sha
        if plantuml_enabled is not None:
            self._values["plantuml_enabled"] = plantuml_enabled
        if plantuml_url is not None:
            self._values["plantuml_url"] = plantuml_url
        if polling_interval_multiplier is not None:
            self._values["polling_interval_multiplier"] = polling_interval_multiplier
        if project_export_enabled is not None:
            self._values["project_export_enabled"] = project_export_enabled
        if prometheus_metrics_enabled is not None:
            self._values["prometheus_metrics_enabled"] = prometheus_metrics_enabled
        if protected_ci_variables is not None:
            self._values["protected_ci_variables"] = protected_ci_variables
        if push_event_activities_limit is not None:
            self._values["push_event_activities_limit"] = push_event_activities_limit
        if push_event_hooks_limit is not None:
            self._values["push_event_hooks_limit"] = push_event_hooks_limit
        if pypi_package_requests_forwarding is not None:
            self._values["pypi_package_requests_forwarding"] = pypi_package_requests_forwarding
        if rate_limiting_response_text is not None:
            self._values["rate_limiting_response_text"] = rate_limiting_response_text
        if raw_blob_request_limit is not None:
            self._values["raw_blob_request_limit"] = raw_blob_request_limit
        if recaptcha_enabled is not None:
            self._values["recaptcha_enabled"] = recaptcha_enabled
        if recaptcha_private_key is not None:
            self._values["recaptcha_private_key"] = recaptcha_private_key
        if recaptcha_site_key is not None:
            self._values["recaptcha_site_key"] = recaptcha_site_key
        if receive_max_input_size is not None:
            self._values["receive_max_input_size"] = receive_max_input_size
        if repository_checks_enabled is not None:
            self._values["repository_checks_enabled"] = repository_checks_enabled
        if repository_size_limit is not None:
            self._values["repository_size_limit"] = repository_size_limit
        if repository_storages is not None:
            self._values["repository_storages"] = repository_storages
        if repository_storages_weighted is not None:
            self._values["repository_storages_weighted"] = repository_storages_weighted
        if require_admin_approval_after_user_signup is not None:
            self._values["require_admin_approval_after_user_signup"] = require_admin_approval_after_user_signup
        if require_two_factor_authentication is not None:
            self._values["require_two_factor_authentication"] = require_two_factor_authentication
        if restricted_visibility_levels is not None:
            self._values["restricted_visibility_levels"] = restricted_visibility_levels
        if rsa_key_restriction is not None:
            self._values["rsa_key_restriction"] = rsa_key_restriction
        if search_rate_limit is not None:
            self._values["search_rate_limit"] = search_rate_limit
        if search_rate_limit_unauthenticated is not None:
            self._values["search_rate_limit_unauthenticated"] = search_rate_limit_unauthenticated
        if send_user_confirmation_email is not None:
            self._values["send_user_confirmation_email"] = send_user_confirmation_email
        if session_expire_delay is not None:
            self._values["session_expire_delay"] = session_expire_delay
        if shared_runners_enabled is not None:
            self._values["shared_runners_enabled"] = shared_runners_enabled
        if shared_runners_minutes is not None:
            self._values["shared_runners_minutes"] = shared_runners_minutes
        if shared_runners_text is not None:
            self._values["shared_runners_text"] = shared_runners_text
        if sidekiq_job_limiter_compression_threshold_bytes is not None:
            self._values["sidekiq_job_limiter_compression_threshold_bytes"] = sidekiq_job_limiter_compression_threshold_bytes
        if sidekiq_job_limiter_limit_bytes is not None:
            self._values["sidekiq_job_limiter_limit_bytes"] = sidekiq_job_limiter_limit_bytes
        if sidekiq_job_limiter_mode is not None:
            self._values["sidekiq_job_limiter_mode"] = sidekiq_job_limiter_mode
        if sign_in_text is not None:
            self._values["sign_in_text"] = sign_in_text
        if signup_enabled is not None:
            self._values["signup_enabled"] = signup_enabled
        if slack_app_enabled is not None:
            self._values["slack_app_enabled"] = slack_app_enabled
        if slack_app_id is not None:
            self._values["slack_app_id"] = slack_app_id
        if slack_app_secret is not None:
            self._values["slack_app_secret"] = slack_app_secret
        if slack_app_signing_secret is not None:
            self._values["slack_app_signing_secret"] = slack_app_signing_secret
        if slack_app_verification_token is not None:
            self._values["slack_app_verification_token"] = slack_app_verification_token
        if snippet_size_limit is not None:
            self._values["snippet_size_limit"] = snippet_size_limit
        if snowplow_app_id is not None:
            self._values["snowplow_app_id"] = snowplow_app_id
        if snowplow_collector_hostname is not None:
            self._values["snowplow_collector_hostname"] = snowplow_collector_hostname
        if snowplow_cookie_domain is not None:
            self._values["snowplow_cookie_domain"] = snowplow_cookie_domain
        if snowplow_enabled is not None:
            self._values["snowplow_enabled"] = snowplow_enabled
        if sourcegraph_enabled is not None:
            self._values["sourcegraph_enabled"] = sourcegraph_enabled
        if sourcegraph_public_only is not None:
            self._values["sourcegraph_public_only"] = sourcegraph_public_only
        if sourcegraph_url is not None:
            self._values["sourcegraph_url"] = sourcegraph_url
        if spam_check_api_key is not None:
            self._values["spam_check_api_key"] = spam_check_api_key
        if spam_check_endpoint_enabled is not None:
            self._values["spam_check_endpoint_enabled"] = spam_check_endpoint_enabled
        if spam_check_endpoint_url is not None:
            self._values["spam_check_endpoint_url"] = spam_check_endpoint_url
        if suggest_pipeline_enabled is not None:
            self._values["suggest_pipeline_enabled"] = suggest_pipeline_enabled
        if terminal_max_session_time is not None:
            self._values["terminal_max_session_time"] = terminal_max_session_time
        if terms is not None:
            self._values["terms"] = terms
        if throttle_authenticated_api_enabled is not None:
            self._values["throttle_authenticated_api_enabled"] = throttle_authenticated_api_enabled
        if throttle_authenticated_api_period_in_seconds is not None:
            self._values["throttle_authenticated_api_period_in_seconds"] = throttle_authenticated_api_period_in_seconds
        if throttle_authenticated_api_requests_per_period is not None:
            self._values["throttle_authenticated_api_requests_per_period"] = throttle_authenticated_api_requests_per_period
        if throttle_authenticated_packages_api_enabled is not None:
            self._values["throttle_authenticated_packages_api_enabled"] = throttle_authenticated_packages_api_enabled
        if throttle_authenticated_packages_api_period_in_seconds is not None:
            self._values["throttle_authenticated_packages_api_period_in_seconds"] = throttle_authenticated_packages_api_period_in_seconds
        if throttle_authenticated_packages_api_requests_per_period is not None:
            self._values["throttle_authenticated_packages_api_requests_per_period"] = throttle_authenticated_packages_api_requests_per_period
        if throttle_authenticated_web_enabled is not None:
            self._values["throttle_authenticated_web_enabled"] = throttle_authenticated_web_enabled
        if throttle_authenticated_web_period_in_seconds is not None:
            self._values["throttle_authenticated_web_period_in_seconds"] = throttle_authenticated_web_period_in_seconds
        if throttle_authenticated_web_requests_per_period is not None:
            self._values["throttle_authenticated_web_requests_per_period"] = throttle_authenticated_web_requests_per_period
        if throttle_unauthenticated_api_enabled is not None:
            self._values["throttle_unauthenticated_api_enabled"] = throttle_unauthenticated_api_enabled
        if throttle_unauthenticated_api_period_in_seconds is not None:
            self._values["throttle_unauthenticated_api_period_in_seconds"] = throttle_unauthenticated_api_period_in_seconds
        if throttle_unauthenticated_api_requests_per_period is not None:
            self._values["throttle_unauthenticated_api_requests_per_period"] = throttle_unauthenticated_api_requests_per_period
        if throttle_unauthenticated_packages_api_enabled is not None:
            self._values["throttle_unauthenticated_packages_api_enabled"] = throttle_unauthenticated_packages_api_enabled
        if throttle_unauthenticated_packages_api_period_in_seconds is not None:
            self._values["throttle_unauthenticated_packages_api_period_in_seconds"] = throttle_unauthenticated_packages_api_period_in_seconds
        if throttle_unauthenticated_packages_api_requests_per_period is not None:
            self._values["throttle_unauthenticated_packages_api_requests_per_period"] = throttle_unauthenticated_packages_api_requests_per_period
        if throttle_unauthenticated_web_enabled is not None:
            self._values["throttle_unauthenticated_web_enabled"] = throttle_unauthenticated_web_enabled
        if throttle_unauthenticated_web_period_in_seconds is not None:
            self._values["throttle_unauthenticated_web_period_in_seconds"] = throttle_unauthenticated_web_period_in_seconds
        if throttle_unauthenticated_web_requests_per_period is not None:
            self._values["throttle_unauthenticated_web_requests_per_period"] = throttle_unauthenticated_web_requests_per_period
        if time_tracking_limit_to_hours is not None:
            self._values["time_tracking_limit_to_hours"] = time_tracking_limit_to_hours
        if two_factor_grace_period is not None:
            self._values["two_factor_grace_period"] = two_factor_grace_period
        if unique_ips_limit_enabled is not None:
            self._values["unique_ips_limit_enabled"] = unique_ips_limit_enabled
        if unique_ips_limit_per_user is not None:
            self._values["unique_ips_limit_per_user"] = unique_ips_limit_per_user
        if unique_ips_limit_time_window is not None:
            self._values["unique_ips_limit_time_window"] = unique_ips_limit_time_window
        if usage_ping_enabled is not None:
            self._values["usage_ping_enabled"] = usage_ping_enabled
        if user_deactivation_emails_enabled is not None:
            self._values["user_deactivation_emails_enabled"] = user_deactivation_emails_enabled
        if user_default_external is not None:
            self._values["user_default_external"] = user_default_external
        if user_default_internal_regex is not None:
            self._values["user_default_internal_regex"] = user_default_internal_regex
        if user_oauth_applications is not None:
            self._values["user_oauth_applications"] = user_oauth_applications
        if user_show_add_ssh_key_message is not None:
            self._values["user_show_add_ssh_key_message"] = user_show_add_ssh_key_message
        if version_check_enabled is not None:
            self._values["version_check_enabled"] = version_check_enabled
        if web_ide_clientside_preview_enabled is not None:
            self._values["web_ide_clientside_preview_enabled"] = web_ide_clientside_preview_enabled
        if whats_new_variant is not None:
            self._values["whats_new_variant"] = whats_new_variant
        if wiki_page_max_content_bytes is not None:
            self._values["wiki_page_max_content_bytes"] = wiki_page_max_content_bytes

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def abuse_notification_email(self) -> typing.Optional[builtins.str]:
        '''If set, abuse reports are sent to this address. Abuse reports are always available in the Admin Area.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#abuse_notification_email ApplicationSettings#abuse_notification_email}
        '''
        result = self._values.get("abuse_notification_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def admin_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require administrators to enable Admin Mode by re-authenticating for administrative tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#admin_mode ApplicationSettings#admin_mode}
        '''
        result = self._values.get("admin_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def after_sign_out_path(self) -> typing.Optional[builtins.str]:
        '''Where to redirect users after logout.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#after_sign_out_path ApplicationSettings#after_sign_out_path}
        '''
        result = self._values.get("after_sign_out_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def after_sign_up_text(self) -> typing.Optional[builtins.str]:
        '''Text shown to the user after signing up.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#after_sign_up_text ApplicationSettings#after_sign_up_text}
        '''
        result = self._values.get("after_sign_up_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def akismet_api_key(self) -> typing.Optional[builtins.str]:
        '''API key for Akismet spam protection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#akismet_api_key ApplicationSettings#akismet_api_key}
        '''
        result = self._values.get("akismet_api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def akismet_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: akismet_api_key) Enable or disable Akismet spam protection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#akismet_enabled ApplicationSettings#akismet_enabled}
        '''
        result = self._values.get("akismet_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_group_owners_to_manage_ldap(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to allow group owners to manage LDAP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#allow_group_owners_to_manage_ldap ApplicationSettings#allow_group_owners_to_manage_ldap}
        '''
        result = self._values.get("allow_group_owners_to_manage_ldap")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_local_requests_from_system_hooks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow requests to the local network from system hooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#allow_local_requests_from_system_hooks ApplicationSettings#allow_local_requests_from_system_hooks}
        '''
        result = self._values.get("allow_local_requests_from_system_hooks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_local_requests_from_web_hooks_and_services(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow requests to the local network from web hooks and services.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#allow_local_requests_from_web_hooks_and_services ApplicationSettings#allow_local_requests_from_web_hooks_and_services}
        '''
        result = self._values.get("allow_local_requests_from_web_hooks_and_services")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def archive_builds_in_human_readable(self) -> typing.Optional[builtins.str]:
        '''Set the duration for which the jobs are considered as old and expired.

        After that time passes, the jobs are archived and no longer able to be retried. Make it empty to never expire jobs. It has to be no less than 1 day, for example: 15 days, 1 month, 2 years.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#archive_builds_in_human_readable ApplicationSettings#archive_builds_in_human_readable}
        '''
        result = self._values.get("archive_builds_in_human_readable")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_proxy_allowlist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Assets that match these domains are not proxied.

        Wildcards allowed. Your GitLab installation URL is automatically allowlisted. GitLab restart is required to apply changes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_allowlist ApplicationSettings#asset_proxy_allowlist}
        '''
        result = self._values.get("asset_proxy_allowlist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def asset_proxy_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: asset_proxy_url) Enable proxying of assets. GitLab restart is required to apply changes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_enabled ApplicationSettings#asset_proxy_enabled}
        '''
        result = self._values.get("asset_proxy_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def asset_proxy_secret_key(self) -> typing.Optional[builtins.str]:
        '''Shared secret with the asset proxy server. GitLab restart is required to apply changes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_secret_key ApplicationSettings#asset_proxy_secret_key}
        '''
        result = self._values.get("asset_proxy_secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_proxy_url(self) -> typing.Optional[builtins.str]:
        '''URL of the asset proxy server. GitLab restart is required to apply changes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#asset_proxy_url ApplicationSettings#asset_proxy_url}
        '''
        result = self._values.get("asset_proxy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorized_keys_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''By default, we write to the authorized_keys file to support Git over SSH without additional configuration.

        GitLab can be optimized to authenticate SSH keys via the database file. Only disable this if you have configured your OpenSSH server to use the AuthorizedKeysCommand.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#authorized_keys_enabled ApplicationSettings#authorized_keys_enabled}
        '''
        result = self._values.get("authorized_keys_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_devops_domain(self) -> typing.Optional[builtins.str]:
        '''Specify a domain to use by default for every project’s Auto Review Apps and Auto Deploy stages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#auto_devops_domain ApplicationSettings#auto_devops_domain}
        '''
        result = self._values.get("auto_devops_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_devops_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Auto DevOps for projects by default.

        It automatically builds, tests, and deploys applications based on a predefined CI/CD configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#auto_devops_enabled ApplicationSettings#auto_devops_enabled}
        '''
        result = self._values.get("auto_devops_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def automatic_purchased_storage_allocation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enabling this permits automatic allocation of purchased storage in a namespace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#automatic_purchased_storage_allocation ApplicationSettings#automatic_purchased_storage_allocation}
        '''
        result = self._values.get("automatic_purchased_storage_allocation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def can_create_group(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether users can create top-level groups. Introduced in GitLab 15.5.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#can_create_group ApplicationSettings#can_create_group}
        '''
        result = self._values.get("can_create_group")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def check_namespace_plan(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enabling this makes only licensed EE features available to projects if the project namespace’s plan includes the feature or if the project is public.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#check_namespace_plan ApplicationSettings#check_namespace_plan}
        '''
        result = self._values.get("check_namespace_plan")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def commit_email_hostname(self) -> typing.Optional[builtins.str]:
        '''Custom hostname (for private commit emails).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#commit_email_hostname ApplicationSettings#commit_email_hostname}
        '''
        result = self._values.get("commit_email_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_expiration_policies_enable_historic_entries(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable cleanup policies for all projects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_expiration_policies_enable_historic_entries ApplicationSettings#container_expiration_policies_enable_historic_entries}
        '''
        result = self._values.get("container_expiration_policies_enable_historic_entries")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def container_registry_cleanup_tags_service_max_list_size(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''The maximum number of tags that can be deleted in a single execution of cleanup policies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_cleanup_tags_service_max_list_size ApplicationSettings#container_registry_cleanup_tags_service_max_list_size}
        '''
        result = self._values.get("container_registry_cleanup_tags_service_max_list_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def container_registry_delete_tags_service_timeout(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''The maximum time, in seconds, that the cleanup process can take to delete a batch of tags for cleanup policies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_delete_tags_service_timeout ApplicationSettings#container_registry_delete_tags_service_timeout}
        '''
        result = self._values.get("container_registry_delete_tags_service_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def container_registry_expiration_policies_caching(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Caching during the execution of cleanup policies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_expiration_policies_caching ApplicationSettings#container_registry_expiration_policies_caching}
        '''
        result = self._values.get("container_registry_expiration_policies_caching")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def container_registry_expiration_policies_worker_capacity(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Number of workers for cleanup policies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_expiration_policies_worker_capacity ApplicationSettings#container_registry_expiration_policies_worker_capacity}
        '''
        result = self._values.get("container_registry_expiration_policies_worker_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def container_registry_token_expire_delay(self) -> typing.Optional[jsii.Number]:
        '''Container Registry token duration in minutes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#container_registry_token_expire_delay ApplicationSettings#container_registry_token_expire_delay}
        '''
        result = self._values.get("container_registry_token_expire_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def deactivate_dormant_users(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable automatic deactivation of dormant users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#deactivate_dormant_users ApplicationSettings#deactivate_dormant_users}
        '''
        result = self._values.get("deactivate_dormant_users")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_artifacts_expire_in(self) -> typing.Optional[builtins.str]:
        '''Set the default expiration time for each job’s artifacts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_artifacts_expire_in ApplicationSettings#default_artifacts_expire_in}
        '''
        result = self._values.get("default_artifacts_expire_in")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_branch_name(self) -> typing.Optional[builtins.str]:
        '''Instance-level custom initial branch name (introduced in GitLab 13.2).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_branch_name ApplicationSettings#default_branch_name}
        '''
        result = self._values.get("default_branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_branch_protection(self) -> typing.Optional[jsii.Number]:
        '''Determine if developers can push to the default branch.

        Can take: 0 (not protected, both users with the Developer role or Maintainer role can push new commits and force push), 1 (partially protected, users with the Developer role or Maintainer role can push new commits, but cannot force push) or 2 (fully protected, users with the Developer or Maintainer role cannot push new commits, but users with the Developer or Maintainer role can; no one can force push) as a parameter. Default is 2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_branch_protection ApplicationSettings#default_branch_protection}
        '''
        result = self._values.get("default_branch_protection")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_ci_config_path(self) -> typing.Optional[builtins.str]:
        '''Default CI/CD configuration file and path for new projects (.gitlab-ci.yml if not set).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_ci_config_path ApplicationSettings#default_ci_config_path}
        '''
        result = self._values.get("default_ci_config_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_group_visibility(self) -> typing.Optional[builtins.str]:
        '''What visibility level new groups receive. Can take private, internal and public as a parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_group_visibility ApplicationSettings#default_group_visibility}
        '''
        result = self._values.get("default_group_visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_project_creation(self) -> typing.Optional[jsii.Number]:
        '''Default project creation protection. Can take: 0 (No one), 1 (Maintainers) or 2 (Developers + Maintainers).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_project_creation ApplicationSettings#default_project_creation}
        '''
        result = self._values.get("default_project_creation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_projects_limit(self) -> typing.Optional[jsii.Number]:
        '''Project limit per user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_projects_limit ApplicationSettings#default_projects_limit}
        '''
        result = self._values.get("default_projects_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_project_visibility(self) -> typing.Optional[builtins.str]:
        '''What visibility level new projects receive. Can take private, internal and public as a parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_project_visibility ApplicationSettings#default_project_visibility}
        '''
        result = self._values.get("default_project_visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_snippet_visibility(self) -> typing.Optional[builtins.str]:
        '''What visibility level new snippets receive. Can take private, internal and public as a parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#default_snippet_visibility ApplicationSettings#default_snippet_visibility}
        '''
        result = self._values.get("default_snippet_visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delayed_group_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable delayed group deletion.

        Introduced in GitLab 15.0. From GitLab 15.1, disables and locks the group-level setting for delayed protect deletion when set to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#delayed_group_deletion ApplicationSettings#delayed_group_deletion}
        '''
        result = self._values.get("delayed_group_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delayed_project_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable delayed project deletion by default in new groups.

        From GitLab 15.1, can only be enabled when delayed_group_deletion is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#delayed_project_deletion ApplicationSettings#delayed_project_deletion}
        '''
        result = self._values.get("delayed_project_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete_inactive_projects(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable inactive project deletion feature. Introduced in GitLab 14.10. Became operational in GitLab 15.0 (with feature flag inactive_projects_deletion).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#delete_inactive_projects ApplicationSettings#delete_inactive_projects}
        '''
        result = self._values.get("delete_inactive_projects")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deletion_adjourned_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days to wait before deleting a project or group that is marked for deletion.

        Value must be between 1 and 90. From GitLab 15.1, a hook on deletion_adjourned_period sets the period to 1 on every update, and sets both delayed_project_deletion and delayed_group_deletion to false if the period is 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#deletion_adjourned_period ApplicationSettings#deletion_adjourned_period}
        '''
        result = self._values.get("deletion_adjourned_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def diff_max_files(self) -> typing.Optional[jsii.Number]:
        '''Maximum files in a diff.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#diff_max_files ApplicationSettings#diff_max_files}
        '''
        result = self._values.get("diff_max_files")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def diff_max_lines(self) -> typing.Optional[jsii.Number]:
        '''Maximum lines in a diff.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#diff_max_lines ApplicationSettings#diff_max_lines}
        '''
        result = self._values.get("diff_max_lines")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def diff_max_patch_bytes(self) -> typing.Optional[jsii.Number]:
        '''Maximum diff patch size, in bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#diff_max_patch_bytes ApplicationSettings#diff_max_patch_bytes}
        '''
        result = self._values.get("diff_max_patch_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disabled_oauth_sign_in_sources(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Disabled OAuth sign-in sources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#disabled_oauth_sign_in_sources ApplicationSettings#disabled_oauth_sign_in_sources}
        '''
        result = self._values.get("disabled_oauth_sign_in_sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def disable_feed_token(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable display of RSS/Atom and calendar feed tokens (introduced in GitLab 13.7).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#disable_feed_token ApplicationSettings#disable_feed_token}
        '''
        result = self._values.get("disable_feed_token")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dns_rebinding_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enforce DNS rebinding attack protection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#dns_rebinding_protection_enabled ApplicationSettings#dns_rebinding_protection_enabled}
        '''
        result = self._values.get("dns_rebinding_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def domain_allowlist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Force people to use only corporate emails for sign-up. Null means there is no restriction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#domain_allowlist ApplicationSettings#domain_allowlist}
        '''
        result = self._values.get("domain_allowlist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domain_denylist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Users with email addresses that match these domains cannot sign up.

        Wildcards allowed. Use separate lines for multiple entries. Ex: domain.com, *.domain.com.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#domain_denylist ApplicationSettings#domain_denylist}
        '''
        result = self._values.get("domain_denylist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domain_denylist_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: domain_denylist) Allows blocking sign-ups from emails from specific domains.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#domain_denylist_enabled ApplicationSettings#domain_denylist_enabled}
        '''
        result = self._values.get("domain_denylist_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dsa_key_restriction(self) -> typing.Optional[jsii.Number]:
        '''The minimum allowed bit length of an uploaded DSA key. 0 means no restriction. -1 disables DSA keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#dsa_key_restriction ApplicationSettings#dsa_key_restriction}
        '''
        result = self._values.get("dsa_key_restriction")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ecdsa_key_restriction(self) -> typing.Optional[jsii.Number]:
        '''The minimum allowed curve size (in bits) of an uploaded ECDSA key.

        0 means no restriction. -1 disables ECDSA keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ecdsa_key_restriction ApplicationSettings#ecdsa_key_restriction}
        '''
        result = self._values.get("ecdsa_key_restriction")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ecdsa_sk_key_restriction(self) -> typing.Optional[jsii.Number]:
        '''The minimum allowed curve size (in bits) of an uploaded ECDSA_SK key.

        0 means no restriction. -1 disables ECDSA_SK keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ecdsa_sk_key_restriction ApplicationSettings#ecdsa_sk_key_restriction}
        '''
        result = self._values.get("ecdsa_sk_key_restriction")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ed25519_key_restriction(self) -> typing.Optional[jsii.Number]:
        '''The minimum allowed curve size (in bits) of an uploaded ED25519 key.

        0 means no restriction. -1 disables ED25519 keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ed25519_key_restriction ApplicationSettings#ed25519_key_restriction}
        '''
        result = self._values.get("ed25519_key_restriction")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ed25519_sk_key_restriction(self) -> typing.Optional[jsii.Number]:
        '''The minimum allowed curve size (in bits) of an uploaded ED25519_SK key.

        0 means no restriction. -1 disables ED25519_SK keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#ed25519_sk_key_restriction ApplicationSettings#ed25519_sk_key_restriction}
        '''
        result = self._values.get("ed25519_sk_key_restriction")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def eks_access_key_id(self) -> typing.Optional[builtins.str]:
        '''AWS IAM access key ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_access_key_id ApplicationSettings#eks_access_key_id}
        '''
        result = self._values.get("eks_access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eks_account_id(self) -> typing.Optional[builtins.str]:
        '''Amazon account ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_account_id ApplicationSettings#eks_account_id}
        '''
        result = self._values.get("eks_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eks_integration_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable integration with Amazon EKS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_integration_enabled ApplicationSettings#eks_integration_enabled}
        '''
        result = self._values.get("eks_integration_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def eks_secret_access_key(self) -> typing.Optional[builtins.str]:
        '''AWS IAM secret access key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#eks_secret_access_key ApplicationSettings#eks_secret_access_key}
        '''
        result = self._values.get("eks_secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_aws(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable the use of AWS hosted Elasticsearch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws ApplicationSettings#elasticsearch_aws}
        '''
        result = self._values.get("elasticsearch_aws")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def elasticsearch_aws_access_key(self) -> typing.Optional[builtins.str]:
        '''AWS IAM access key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws_access_key ApplicationSettings#elasticsearch_aws_access_key}
        '''
        result = self._values.get("elasticsearch_aws_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_aws_region(self) -> typing.Optional[builtins.str]:
        '''The AWS region the Elasticsearch domain is configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws_region ApplicationSettings#elasticsearch_aws_region}
        '''
        result = self._values.get("elasticsearch_aws_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_aws_secret_access_key(self) -> typing.Optional[builtins.str]:
        '''AWS IAM secret access key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_aws_secret_access_key ApplicationSettings#elasticsearch_aws_secret_access_key}
        '''
        result = self._values.get("elasticsearch_aws_secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_indexed_field_length_limit(self) -> typing.Optional[jsii.Number]:
        '''Maximum size of text fields to index by Elasticsearch.

        0 value means no limit. This does not apply to repository and wiki indexing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_indexed_field_length_limit ApplicationSettings#elasticsearch_indexed_field_length_limit}
        '''
        result = self._values.get("elasticsearch_indexed_field_length_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def elasticsearch_indexed_file_size_limit_kb(self) -> typing.Optional[jsii.Number]:
        '''Maximum size of repository and wiki files that are indexed by Elasticsearch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_indexed_file_size_limit_kb ApplicationSettings#elasticsearch_indexed_file_size_limit_kb}
        '''
        result = self._values.get("elasticsearch_indexed_file_size_limit_kb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def elasticsearch_indexing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Elasticsearch indexing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_indexing ApplicationSettings#elasticsearch_indexing}
        '''
        result = self._values.get("elasticsearch_indexing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def elasticsearch_limit_indexing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Limit Elasticsearch to index certain namespaces and projects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_limit_indexing ApplicationSettings#elasticsearch_limit_indexing}
        '''
        result = self._values.get("elasticsearch_limit_indexing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def elasticsearch_max_bulk_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Maximum concurrency of Elasticsearch bulk requests per indexing operation. This only applies to repository indexing operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_max_bulk_concurrency ApplicationSettings#elasticsearch_max_bulk_concurrency}
        '''
        result = self._values.get("elasticsearch_max_bulk_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def elasticsearch_max_bulk_size_mb(self) -> typing.Optional[jsii.Number]:
        '''Maximum size of Elasticsearch bulk indexing requests in MB. This only applies to repository indexing operations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_max_bulk_size_mb ApplicationSettings#elasticsearch_max_bulk_size_mb}
        '''
        result = self._values.get("elasticsearch_max_bulk_size_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def elasticsearch_namespace_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The namespaces to index via Elasticsearch if elasticsearch_limit_indexing is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_namespace_ids ApplicationSettings#elasticsearch_namespace_ids}
        '''
        result = self._values.get("elasticsearch_namespace_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def elasticsearch_password(self) -> typing.Optional[builtins.str]:
        '''The password of your Elasticsearch instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_password ApplicationSettings#elasticsearch_password}
        '''
        result = self._values.get("elasticsearch_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch_project_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The projects to index via Elasticsearch if elasticsearch_limit_indexing is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_project_ids ApplicationSettings#elasticsearch_project_ids}
        '''
        result = self._values.get("elasticsearch_project_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def elasticsearch_search(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Elasticsearch search.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_search ApplicationSettings#elasticsearch_search}
        '''
        result = self._values.get("elasticsearch_search")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def elasticsearch_url(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The URL to use for connecting to Elasticsearch. Use a comma-separated list to support cluster (for example, http://localhost:9200, http://localhost:9201).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_url ApplicationSettings#elasticsearch_url}
        '''
        result = self._values.get("elasticsearch_url")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def elasticsearch_username(self) -> typing.Optional[builtins.str]:
        '''The username of your Elasticsearch instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#elasticsearch_username ApplicationSettings#elasticsearch_username}
        '''
        result = self._values.get("elasticsearch_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_additional_text(self) -> typing.Optional[builtins.str]:
        '''Additional text added to the bottom of every email for legal/auditing/compliance reasons.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#email_additional_text ApplicationSettings#email_additional_text}
        '''
        result = self._values.get("email_additional_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_author_in_body(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Some email servers do not support overriding the email sender name.

        Enable this option to include the name of the author of the issue, merge request or comment in the email body instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#email_author_in_body ApplicationSettings#email_author_in_body}
        '''
        result = self._values.get("email_author_in_body")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enabled_git_access_protocol(self) -> typing.Optional[builtins.str]:
        '''Enabled protocols for Git access. Allowed values are: ssh, http, and nil to allow both protocols.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#enabled_git_access_protocol ApplicationSettings#enabled_git_access_protocol}
        '''
        result = self._values.get("enabled_git_access_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_namespace_storage_limit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enabling this permits enforcement of namespace storage limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#enforce_namespace_storage_limit ApplicationSettings#enforce_namespace_storage_limit}
        '''
        result = self._values.get("enforce_namespace_storage_limit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enforce_terms(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: terms) Enforce application ToS to all users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#enforce_terms ApplicationSettings#enforce_terms}
        '''
        result = self._values.get("enforce_terms")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_auth_client_cert(self) -> typing.Optional[builtins.str]:
        '''(If enabled, requires: external_auth_client_key) The certificate to use to authenticate with the external authorization service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_auth_client_cert ApplicationSettings#external_auth_client_cert}
        '''
        result = self._values.get("external_auth_client_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_auth_client_key(self) -> typing.Optional[builtins.str]:
        '''Private key for the certificate when authentication is required for the external authorization service, this is encrypted when stored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_auth_client_key ApplicationSettings#external_auth_client_key}
        '''
        result = self._values.get("external_auth_client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_auth_client_key_pass(self) -> typing.Optional[builtins.str]:
        '''Passphrase to use for the private key when authenticating with the external service this is encrypted when stored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_auth_client_key_pass ApplicationSettings#external_auth_client_key_pass}
        '''
        result = self._values.get("external_auth_client_key_pass")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_authorization_service_default_label(
        self,
    ) -> typing.Optional[builtins.str]:
        '''The default classification label to use when requesting authorization and no classification label has been specified on the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_default_label ApplicationSettings#external_authorization_service_default_label}
        '''
        result = self._values.get("external_authorization_service_default_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_authorization_service_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: external_authorization_service_default_label, external_authorization_service_timeout and external_authorization_service_url) Enable using an external authorization service for accessing projects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_enabled ApplicationSettings#external_authorization_service_enabled}
        '''
        result = self._values.get("external_authorization_service_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_authorization_service_timeout(self) -> typing.Optional[jsii.Number]:
        '''The timeout after which an authorization request is aborted, in seconds.

        When a request times out, access is denied to the user. (min: 0.001, max: 10, step: 0.001).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_timeout ApplicationSettings#external_authorization_service_timeout}
        '''
        result = self._values.get("external_authorization_service_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_authorization_service_url(self) -> typing.Optional[builtins.str]:
        '''URL to which authorization requests are directed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_authorization_service_url ApplicationSettings#external_authorization_service_url}
        '''
        result = self._values.get("external_authorization_service_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_pipeline_validation_service_timeout(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''How long to wait for a response from the pipeline validation service. Assumes OK if it times out.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_pipeline_validation_service_timeout ApplicationSettings#external_pipeline_validation_service_timeout}
        '''
        result = self._values.get("external_pipeline_validation_service_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external_pipeline_validation_service_token(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Optional. Token to include as the X-Gitlab-Token header in requests to the URL in external_pipeline_validation_service_url.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_pipeline_validation_service_token ApplicationSettings#external_pipeline_validation_service_token}
        '''
        result = self._values.get("external_pipeline_validation_service_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_pipeline_validation_service_url(self) -> typing.Optional[builtins.str]:
        '''URL to use for pipeline validation requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#external_pipeline_validation_service_url ApplicationSettings#external_pipeline_validation_service_url}
        '''
        result = self._values.get("external_pipeline_validation_service_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_template_project_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of a project to load custom file templates from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#file_template_project_id ApplicationSettings#file_template_project_id}
        '''
        result = self._values.get("file_template_project_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def first_day_of_week(self) -> typing.Optional[jsii.Number]:
        '''Start day of the week for calendar views and date pickers.

        Valid values are 0 for Sunday, 1 for Monday, and 6 for Saturday.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#first_day_of_week ApplicationSettings#first_day_of_week}
        '''
        result = self._values.get("first_day_of_week")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def geo_node_allowed_ips(self) -> typing.Optional[builtins.str]:
        '''Comma-separated list of IPs and CIDRs of allowed secondary nodes. For example, 1.1.1.1, 2.2.2.0/24.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#geo_node_allowed_ips ApplicationSettings#geo_node_allowed_ips}
        '''
        result = self._values.get("geo_node_allowed_ips")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geo_status_timeout(self) -> typing.Optional[jsii.Number]:
        '''The amount of seconds after which a request to get a secondary node status times out.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#geo_status_timeout ApplicationSettings#geo_status_timeout}
        '''
        result = self._values.get("geo_status_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gitaly_timeout_default(self) -> typing.Optional[jsii.Number]:
        '''Default Gitaly timeout, in seconds.

        This timeout is not enforced for Git fetch/push operations or Sidekiq jobs. Set to 0 to disable timeouts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gitaly_timeout_default ApplicationSettings#gitaly_timeout_default}
        '''
        result = self._values.get("gitaly_timeout_default")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gitaly_timeout_fast(self) -> typing.Optional[jsii.Number]:
        '''Gitaly fast operation timeout, in seconds.

        Some Gitaly operations are expected to be fast. If they exceed this threshold, there may be a problem with a storage shard and ‘failing fast’ can help maintain the stability of the GitLab instance. Set to 0 to disable timeouts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gitaly_timeout_fast ApplicationSettings#gitaly_timeout_fast}
        '''
        result = self._values.get("gitaly_timeout_fast")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gitaly_timeout_medium(self) -> typing.Optional[jsii.Number]:
        '''Medium Gitaly timeout, in seconds.

        This should be a value between the Fast and the Default timeout. Set to 0 to disable timeouts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gitaly_timeout_medium ApplicationSettings#gitaly_timeout_medium}
        '''
        result = self._values.get("gitaly_timeout_medium")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def git_rate_limit_users_allowlist(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''List of usernames excluded from Git anti-abuse rate limits. Maximum: 100 usernames. Introduced in GitLab 15.2.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#git_rate_limit_users_allowlist ApplicationSettings#git_rate_limit_users_allowlist}
        '''
        result = self._values.get("git_rate_limit_users_allowlist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def git_two_factor_session_expiry(self) -> typing.Optional[jsii.Number]:
        '''Maximum duration (in minutes) of a session for Git operations when 2FA is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#git_two_factor_session_expiry ApplicationSettings#git_two_factor_session_expiry}
        '''
        result = self._values.get("git_two_factor_session_expiry")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grafana_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Grafana.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#grafana_enabled ApplicationSettings#grafana_enabled}
        '''
        result = self._values.get("grafana_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def grafana_url(self) -> typing.Optional[builtins.str]:
        '''Grafana URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#grafana_url ApplicationSettings#grafana_url}
        '''
        result = self._values.get("grafana_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gravatar_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Gravatar.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#gravatar_enabled ApplicationSettings#gravatar_enabled}
        '''
        result = self._values.get("gravatar_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def group_owners_can_manage_default_branch_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent overrides of default branch protection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#group_owners_can_manage_default_branch_protection ApplicationSettings#group_owners_can_manage_default_branch_protection}
        '''
        result = self._values.get("group_owners_can_manage_default_branch_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hashed_storage_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Create new projects using hashed storage paths: Enable immutable, hash-based paths and repository names to store repositories on disk.

        This prevents repositories from having to be moved or renamed when the Project URL changes and may improve disk I/O performance. (Always enabled in GitLab versions 13.0 and later, configuration is scheduled for removal in 14.0).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#hashed_storage_enabled ApplicationSettings#hashed_storage_enabled}
        '''
        result = self._values.get("hashed_storage_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def help_page_hide_commercial_content(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Hide marketing-related entries from help.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_page_hide_commercial_content ApplicationSettings#help_page_hide_commercial_content}
        '''
        result = self._values.get("help_page_hide_commercial_content")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def help_page_support_url(self) -> typing.Optional[builtins.str]:
        '''Alternate support URL for help page and help dropdown.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_page_support_url ApplicationSettings#help_page_support_url}
        '''
        result = self._values.get("help_page_support_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def help_page_text(self) -> typing.Optional[builtins.str]:
        '''Custom text displayed on the help page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_page_text ApplicationSettings#help_page_text}
        '''
        result = self._values.get("help_page_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def help_text(self) -> typing.Optional[builtins.str]:
        '''GitLab server administrator information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#help_text ApplicationSettings#help_text}
        '''
        result = self._values.get("help_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hide_third_party_offers(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not display offers from third parties in GitLab.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#hide_third_party_offers ApplicationSettings#hide_third_party_offers}
        '''
        result = self._values.get("hide_third_party_offers")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def home_page_url(self) -> typing.Optional[builtins.str]:
        '''Redirect to this URL when not logged in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#home_page_url ApplicationSettings#home_page_url}
        '''
        result = self._values.get("home_page_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def housekeeping_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: housekeeping_bitmaps_enabled, housekeeping_full_repack_period, housekeeping_gc_period, and housekeeping_incremental_repack_period) Enable or disable Git housekeeping.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_enabled ApplicationSettings#housekeeping_enabled}
        '''
        result = self._values.get("housekeeping_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def housekeeping_full_repack_period(self) -> typing.Optional[jsii.Number]:
        '''Number of Git pushes after which an incremental git repack is run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_full_repack_period ApplicationSettings#housekeeping_full_repack_period}
        '''
        result = self._values.get("housekeeping_full_repack_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def housekeeping_gc_period(self) -> typing.Optional[jsii.Number]:
        '''Number of Git pushes after which git gc is run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_gc_period ApplicationSettings#housekeeping_gc_period}
        '''
        result = self._values.get("housekeeping_gc_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def housekeeping_incremental_repack_period(self) -> typing.Optional[jsii.Number]:
        '''Number of Git pushes after which an incremental git repack is run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#housekeeping_incremental_repack_period ApplicationSettings#housekeeping_incremental_repack_period}
        '''
        result = self._values.get("housekeeping_incremental_repack_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def html_emails_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable HTML emails.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#html_emails_enabled ApplicationSettings#html_emails_enabled}
        '''
        result = self._values.get("html_emails_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#id ApplicationSettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def import_sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Sources to allow project import from. Valid values are: ``github``, ``bitbucket``, ``bitbucket_server``, ``fogbugz``, ``git``, ``gitlab_project``, ``gitea``, ``manifest``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#import_sources ApplicationSettings#import_sources}
        '''
        result = self._values.get("import_sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inactive_projects_delete_after_months(self) -> typing.Optional[jsii.Number]:
        '''If delete_inactive_projects is true, the time (in months) to wait before deleting inactive projects.

        Introduced in GitLab 14.10. Became operational in GitLab 15.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#inactive_projects_delete_after_months ApplicationSettings#inactive_projects_delete_after_months}
        '''
        result = self._values.get("inactive_projects_delete_after_months")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def inactive_projects_min_size_mb(self) -> typing.Optional[jsii.Number]:
        '''If delete_inactive_projects is true, the minimum repository size for projects to be checked for inactivity.

        Introduced in GitLab 14.10. Became operational in GitLab 15.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#inactive_projects_min_size_mb ApplicationSettings#inactive_projects_min_size_mb}
        '''
        result = self._values.get("inactive_projects_min_size_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def inactive_projects_send_warning_email_after_months(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''If delete_inactive_projects is true, sets the time (in months) to wait before emailing maintainers that the project is scheduled be deleted because it is inactive.

        Introduced in GitLab 14.10. Became operational in GitLab 15.0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#inactive_projects_send_warning_email_after_months ApplicationSettings#inactive_projects_send_warning_email_after_months}
        '''
        result = self._values.get("inactive_projects_send_warning_email_after_months")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def in_product_marketing_emails_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable in-product marketing emails.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#in_product_marketing_emails_enabled ApplicationSettings#in_product_marketing_emails_enabled}
        '''
        result = self._values.get("in_product_marketing_emails_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def invisible_captcha_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Invisible CAPTCHA spam detection during sign-up.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#invisible_captcha_enabled ApplicationSettings#invisible_captcha_enabled}
        '''
        result = self._values.get("invisible_captcha_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def issues_create_limit(self) -> typing.Optional[jsii.Number]:
        '''Max number of issue creation requests per minute per user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#issues_create_limit ApplicationSettings#issues_create_limit}
        '''
        result = self._values.get("issues_create_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def keep_latest_artifact(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent the deletion of the artifacts from the most recent successful jobs, regardless of the expiry time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#keep_latest_artifact ApplicationSettings#keep_latest_artifact}
        '''
        result = self._values.get("keep_latest_artifact")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def local_markdown_version(self) -> typing.Optional[jsii.Number]:
        '''Increase this value when any cached Markdown should be invalidated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#local_markdown_version ApplicationSettings#local_markdown_version}
        '''
        result = self._values.get("local_markdown_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mailgun_events_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Mailgun event receiver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mailgun_events_enabled ApplicationSettings#mailgun_events_enabled}
        '''
        result = self._values.get("mailgun_events_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mailgun_signing_key(self) -> typing.Optional[builtins.str]:
        '''The Mailgun HTTP webhook signing key for receiving events from webhook.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mailgun_signing_key ApplicationSettings#mailgun_signing_key}
        '''
        result = self._values.get("mailgun_signing_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When instance is in maintenance mode, non-administrative users can sign in with read-only access and make read-only API requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#maintenance_mode ApplicationSettings#maintenance_mode}
        '''
        result = self._values.get("maintenance_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def maintenance_mode_message(self) -> typing.Optional[builtins.str]:
        '''Message displayed when instance is in maintenance mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#maintenance_mode_message ApplicationSettings#maintenance_mode_message}
        '''
        result = self._values.get("maintenance_mode_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_artifacts_size(self) -> typing.Optional[jsii.Number]:
        '''Maximum artifacts size in MB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_artifacts_size ApplicationSettings#max_artifacts_size}
        '''
        result = self._values.get("max_artifacts_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_attachment_size(self) -> typing.Optional[jsii.Number]:
        '''Limit attachment size in MB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_attachment_size ApplicationSettings#max_attachment_size}
        '''
        result = self._values.get("max_attachment_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_export_size(self) -> typing.Optional[jsii.Number]:
        '''Maximum export size in MB. 0 for unlimited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_export_size ApplicationSettings#max_export_size}
        '''
        result = self._values.get("max_export_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_import_size(self) -> typing.Optional[jsii.Number]:
        '''Maximum import size in MB. 0 for unlimited.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_import_size ApplicationSettings#max_import_size}
        '''
        result = self._values.get("max_import_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_number_of_repository_downloads(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of unique repositories a user can download in the specified time period before they are banned.

        Maximum: 10,000 repositories. Introduced in GitLab 15.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_number_of_repository_downloads ApplicationSettings#max_number_of_repository_downloads}
        '''
        result = self._values.get("max_number_of_repository_downloads")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_number_of_repository_downloads_within_time_period(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Reporting time period (in seconds). Maximum: 864000 seconds (10 days). Introduced in GitLab 15.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_number_of_repository_downloads_within_time_period ApplicationSettings#max_number_of_repository_downloads_within_time_period}
        '''
        result = self._values.get("max_number_of_repository_downloads_within_time_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pages_size(self) -> typing.Optional[jsii.Number]:
        '''Maximum size of pages repositories in MB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_pages_size ApplicationSettings#max_pages_size}
        '''
        result = self._values.get("max_pages_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_personal_access_token_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum allowable lifetime for access tokens in days.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_personal_access_token_lifetime ApplicationSettings#max_personal_access_token_lifetime}
        '''
        result = self._values.get("max_personal_access_token_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_ssh_key_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum allowable lifetime for SSH keys in days. Introduced in GitLab 14.6.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#max_ssh_key_lifetime ApplicationSettings#max_ssh_key_lifetime}
        '''
        result = self._values.get("max_ssh_key_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metrics_method_call_threshold(self) -> typing.Optional[jsii.Number]:
        '''A method call is only tracked when it takes longer than the given amount of milliseconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#metrics_method_call_threshold ApplicationSettings#metrics_method_call_threshold}
        '''
        result = self._values.get("metrics_method_call_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mirror_available(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow repository mirroring to configured by project Maintainers. If disabled, only Administrators can configure repository mirroring.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_available ApplicationSettings#mirror_available}
        '''
        result = self._values.get("mirror_available")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mirror_capacity_threshold(self) -> typing.Optional[jsii.Number]:
        '''Minimum capacity to be available before scheduling more mirrors preemptively.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_capacity_threshold ApplicationSettings#mirror_capacity_threshold}
        '''
        result = self._values.get("mirror_capacity_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mirror_max_capacity(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of mirrors that can be synchronizing at the same time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_max_capacity ApplicationSettings#mirror_max_capacity}
        '''
        result = self._values.get("mirror_max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mirror_max_delay(self) -> typing.Optional[jsii.Number]:
        '''Maximum time (in minutes) between updates that a mirror can have when scheduled to synchronize.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#mirror_max_delay ApplicationSettings#mirror_max_delay}
        '''
        result = self._values.get("mirror_max_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def npm_package_requests_forwarding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use npmjs.org as a default remote repository when the package is not found in the GitLab Package Registry for npm.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#npm_package_requests_forwarding ApplicationSettings#npm_package_requests_forwarding}
        '''
        result = self._values.get("npm_package_requests_forwarding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def outbound_local_requests_whitelist(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Define a list of trusted domains or IP addresses to which local requests are allowed when local requests for hooks and services are disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#outbound_local_requests_whitelist ApplicationSettings#outbound_local_requests_whitelist}
        '''
        result = self._values.get("outbound_local_requests_whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def package_registry_cleanup_policies_worker_capacity(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Number of workers assigned to the packages cleanup policies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#package_registry_cleanup_policies_worker_capacity ApplicationSettings#package_registry_cleanup_policies_worker_capacity}
        '''
        result = self._values.get("package_registry_cleanup_policies_worker_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pages_domain_verification_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require users to prove ownership of custom domains.

        Domain verification is an essential security measure for public GitLab sites. Users are required to demonstrate they control a domain before it is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#pages_domain_verification_enabled ApplicationSettings#pages_domain_verification_enabled}
        '''
        result = self._values.get("pages_domain_verification_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_authentication_enabled_for_git(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable authentication for Git over HTTP(S) via a GitLab account password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_authentication_enabled_for_git ApplicationSettings#password_authentication_enabled_for_git}
        '''
        result = self._values.get("password_authentication_enabled_for_git")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_authentication_enabled_for_web(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable authentication for the web interface via a GitLab account password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_authentication_enabled_for_web ApplicationSettings#password_authentication_enabled_for_web}
        '''
        result = self._values.get("password_authentication_enabled_for_web")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_lowercase_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether passwords require at least one lowercase letter. Introduced in GitLab 15.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_lowercase_required ApplicationSettings#password_lowercase_required}
        '''
        result = self._values.get("password_lowercase_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_number_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether passwords require at least one number. Introduced in GitLab 15.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_number_required ApplicationSettings#password_number_required}
        '''
        result = self._values.get("password_number_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_symbol_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether passwords require at least one symbol character. Introduced in GitLab 15.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_symbol_required ApplicationSettings#password_symbol_required}
        '''
        result = self._values.get("password_symbol_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_uppercase_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether passwords require at least one uppercase letter. Introduced in GitLab 15.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#password_uppercase_required ApplicationSettings#password_uppercase_required}
        '''
        result = self._values.get("password_uppercase_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def performance_bar_allowed_group_path(self) -> typing.Optional[builtins.str]:
        '''Path of the group that is allowed to toggle the performance bar.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#performance_bar_allowed_group_path ApplicationSettings#performance_bar_allowed_group_path}
        '''
        result = self._values.get("performance_bar_allowed_group_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def personal_access_token_prefix(self) -> typing.Optional[builtins.str]:
        '''Prefix for all generated personal access tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#personal_access_token_prefix ApplicationSettings#personal_access_token_prefix}
        '''
        result = self._values.get("personal_access_token_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline_limit_per_project_user_sha(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of pipeline creation requests per minute per user and commit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#pipeline_limit_per_project_user_sha ApplicationSettings#pipeline_limit_per_project_user_sha}
        '''
        result = self._values.get("pipeline_limit_per_project_user_sha")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def plantuml_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: plantuml_url) Enable PlantUML integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#plantuml_enabled ApplicationSettings#plantuml_enabled}
        '''
        result = self._values.get("plantuml_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def plantuml_url(self) -> typing.Optional[builtins.str]:
        '''The PlantUML instance URL for integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#plantuml_url ApplicationSettings#plantuml_url}
        '''
        result = self._values.get("plantuml_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def polling_interval_multiplier(self) -> typing.Optional[jsii.Number]:
        '''Interval multiplier used by endpoints that perform polling. Set to 0 to disable polling.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#polling_interval_multiplier ApplicationSettings#polling_interval_multiplier}
        '''
        result = self._values.get("polling_interval_multiplier")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project_export_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable project export.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#project_export_enabled ApplicationSettings#project_export_enabled}
        '''
        result = self._values.get("project_export_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prometheus_metrics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable Prometheus metrics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#prometheus_metrics_enabled ApplicationSettings#prometheus_metrics_enabled}
        '''
        result = self._values.get("prometheus_metrics_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def protected_ci_variables(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''CI/CD variables are protected by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#protected_ci_variables ApplicationSettings#protected_ci_variables}
        '''
        result = self._values.get("protected_ci_variables")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def push_event_activities_limit(self) -> typing.Optional[jsii.Number]:
        '''Number of changes (branches or tags) in a single push to determine whether individual push events or bulk push events are created.

        Bulk push events are created if it surpasses that value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#push_event_activities_limit ApplicationSettings#push_event_activities_limit}
        '''
        result = self._values.get("push_event_activities_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def push_event_hooks_limit(self) -> typing.Optional[jsii.Number]:
        '''Number of changes (branches or tags) in a single push to determine whether webhooks and services fire or not.

        Webhooks and services aren’t submitted if it surpasses that value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#push_event_hooks_limit ApplicationSettings#push_event_hooks_limit}
        '''
        result = self._values.get("push_event_hooks_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pypi_package_requests_forwarding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use pypi.org as a default remote repository when the package is not found in the GitLab Package Registry for PyPI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#pypi_package_requests_forwarding ApplicationSettings#pypi_package_requests_forwarding}
        '''
        result = self._values.get("pypi_package_requests_forwarding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rate_limiting_response_text(self) -> typing.Optional[builtins.str]:
        '''When rate limiting is enabled via the throttle_* settings, send this plain text response when a rate limit is exceeded.

        ‘Retry later’ is sent if this is blank.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#rate_limiting_response_text ApplicationSettings#rate_limiting_response_text}
        '''
        result = self._values.get("rate_limiting_response_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_blob_request_limit(self) -> typing.Optional[jsii.Number]:
        '''Max number of requests per minute for each raw path. To disable throttling set to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#raw_blob_request_limit ApplicationSettings#raw_blob_request_limit}
        '''
        result = self._values.get("raw_blob_request_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def recaptcha_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: recaptcha_private_key and recaptcha_site_key) Enable reCAPTCHA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#recaptcha_enabled ApplicationSettings#recaptcha_enabled}
        '''
        result = self._values.get("recaptcha_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def recaptcha_private_key(self) -> typing.Optional[builtins.str]:
        '''Private key for reCAPTCHA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#recaptcha_private_key ApplicationSettings#recaptcha_private_key}
        '''
        result = self._values.get("recaptcha_private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recaptcha_site_key(self) -> typing.Optional[builtins.str]:
        '''Site key for reCAPTCHA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#recaptcha_site_key ApplicationSettings#recaptcha_site_key}
        '''
        result = self._values.get("recaptcha_site_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def receive_max_input_size(self) -> typing.Optional[jsii.Number]:
        '''Maximum push size (MB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#receive_max_input_size ApplicationSettings#receive_max_input_size}
        '''
        result = self._values.get("receive_max_input_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def repository_checks_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''GitLab periodically runs git fsck in all project and wiki repositories to look for silent disk corruption issues.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_checks_enabled ApplicationSettings#repository_checks_enabled}
        '''
        result = self._values.get("repository_checks_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def repository_size_limit(self) -> typing.Optional[jsii.Number]:
        '''Size limit per repository (MB).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_size_limit ApplicationSettings#repository_size_limit}
        '''
        result = self._values.get("repository_size_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def repository_storages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(GitLab 13.0 and earlier) List of names of enabled storage paths, taken from gitlab.yml. New projects are created in one of these stores, chosen at random.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_storages ApplicationSettings#repository_storages}
        '''
        result = self._values.get("repository_storages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def repository_storages_weighted(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        '''(GitLab 13.1 and later) Hash of names of taken from gitlab.yml to weights. New projects are created in one of these stores, chosen by a weighted random selection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#repository_storages_weighted ApplicationSettings#repository_storages_weighted}
        '''
        result = self._values.get("repository_storages_weighted")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], result)

    @builtins.property
    def require_admin_approval_after_user_signup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, any user that signs up for an account using the registration form is placed under a Pending approval state and has to be explicitly approved by an administrator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#require_admin_approval_after_user_signup ApplicationSettings#require_admin_approval_after_user_signup}
        '''
        result = self._values.get("require_admin_approval_after_user_signup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_two_factor_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: two_factor_grace_period) Require all users to set up Two-factor authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#require_two_factor_authentication ApplicationSettings#require_two_factor_authentication}
        '''
        result = self._values.get("require_two_factor_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restricted_visibility_levels(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Selected levels cannot be used by non-Administrator users for groups, projects or snippets.

        Can take private, internal and public as a parameter. Null means there is no restriction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#restricted_visibility_levels ApplicationSettings#restricted_visibility_levels}
        '''
        result = self._values.get("restricted_visibility_levels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rsa_key_restriction(self) -> typing.Optional[jsii.Number]:
        '''The minimum allowed bit length of an uploaded RSA key. 0 means no restriction. -1 disables RSA keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#rsa_key_restriction ApplicationSettings#rsa_key_restriction}
        '''
        result = self._values.get("rsa_key_restriction")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def search_rate_limit(self) -> typing.Optional[jsii.Number]:
        '''Max number of requests per minute for performing a search while authenticated. To disable throttling set to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#search_rate_limit ApplicationSettings#search_rate_limit}
        '''
        result = self._values.get("search_rate_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def search_rate_limit_unauthenticated(self) -> typing.Optional[jsii.Number]:
        '''Max number of requests per minute for performing a search while unauthenticated. To disable throttling set to 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#search_rate_limit_unauthenticated ApplicationSettings#search_rate_limit_unauthenticated}
        '''
        result = self._values.get("search_rate_limit_unauthenticated")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def send_user_confirmation_email(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Send confirmation email on sign-up.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#send_user_confirmation_email ApplicationSettings#send_user_confirmation_email}
        '''
        result = self._values.get("send_user_confirmation_email")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def session_expire_delay(self) -> typing.Optional[jsii.Number]:
        '''Session duration in minutes. GitLab restart is required to apply changes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#session_expire_delay ApplicationSettings#session_expire_delay}
        '''
        result = self._values.get("session_expire_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def shared_runners_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: shared_runners_text and shared_runners_minutes) Enable shared runners for new projects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#shared_runners_enabled ApplicationSettings#shared_runners_enabled}
        '''
        result = self._values.get("shared_runners_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def shared_runners_minutes(self) -> typing.Optional[jsii.Number]:
        '''Set the maximum number of CI/CD minutes that a group can use on shared runners per month.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#shared_runners_minutes ApplicationSettings#shared_runners_minutes}
        '''
        result = self._values.get("shared_runners_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def shared_runners_text(self) -> typing.Optional[builtins.str]:
        '''Shared runners text.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#shared_runners_text ApplicationSettings#shared_runners_text}
        '''
        result = self._values.get("shared_runners_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sidekiq_job_limiter_compression_threshold_bytes(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''The threshold in bytes at which Sidekiq jobs are compressed before being stored in Redis.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sidekiq_job_limiter_compression_threshold_bytes ApplicationSettings#sidekiq_job_limiter_compression_threshold_bytes}
        '''
        result = self._values.get("sidekiq_job_limiter_compression_threshold_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sidekiq_job_limiter_limit_bytes(self) -> typing.Optional[jsii.Number]:
        '''The threshold in bytes at which Sidekiq jobs are rejected. 0 means do not reject any job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sidekiq_job_limiter_limit_bytes ApplicationSettings#sidekiq_job_limiter_limit_bytes}
        '''
        result = self._values.get("sidekiq_job_limiter_limit_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sidekiq_job_limiter_mode(self) -> typing.Optional[builtins.str]:
        '''track or compress. Sets the behavior for Sidekiq job size limits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sidekiq_job_limiter_mode ApplicationSettings#sidekiq_job_limiter_mode}
        '''
        result = self._values.get("sidekiq_job_limiter_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sign_in_text(self) -> typing.Optional[builtins.str]:
        '''Text on the login page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sign_in_text ApplicationSettings#sign_in_text}
        '''
        result = self._values.get("sign_in_text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable registration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#signup_enabled ApplicationSettings#signup_enabled}
        '''
        result = self._values.get("signup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def slack_app_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: slack_app_id, slack_app_secret and slack_app_secret) Enable Slack app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_enabled ApplicationSettings#slack_app_enabled}
        '''
        result = self._values.get("slack_app_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def slack_app_id(self) -> typing.Optional[builtins.str]:
        '''The app ID of the Slack-app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_id ApplicationSettings#slack_app_id}
        '''
        result = self._values.get("slack_app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_app_secret(self) -> typing.Optional[builtins.str]:
        '''The app secret of the Slack-app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_secret ApplicationSettings#slack_app_secret}
        '''
        result = self._values.get("slack_app_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_app_signing_secret(self) -> typing.Optional[builtins.str]:
        '''The signing secret of the Slack-app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_signing_secret ApplicationSettings#slack_app_signing_secret}
        '''
        result = self._values.get("slack_app_signing_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_app_verification_token(self) -> typing.Optional[builtins.str]:
        '''The verification token of the Slack-app.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#slack_app_verification_token ApplicationSettings#slack_app_verification_token}
        '''
        result = self._values.get("slack_app_verification_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snippet_size_limit(self) -> typing.Optional[jsii.Number]:
        '''Max snippet content size in bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snippet_size_limit ApplicationSettings#snippet_size_limit}
        '''
        result = self._values.get("snippet_size_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snowplow_app_id(self) -> typing.Optional[builtins.str]:
        '''The Snowplow site name / application ID. (for example, gitlab).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_app_id ApplicationSettings#snowplow_app_id}
        '''
        result = self._values.get("snowplow_app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snowplow_collector_hostname(self) -> typing.Optional[builtins.str]:
        '''The Snowplow collector hostname. (for example, snowplow.trx.gitlab.net).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_collector_hostname ApplicationSettings#snowplow_collector_hostname}
        '''
        result = self._values.get("snowplow_collector_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snowplow_cookie_domain(self) -> typing.Optional[builtins.str]:
        '''The Snowplow cookie domain. (for example, .gitlab.com).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_cookie_domain ApplicationSettings#snowplow_cookie_domain}
        '''
        result = self._values.get("snowplow_cookie_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snowplow_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable snowplow tracking.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#snowplow_enabled ApplicationSettings#snowplow_enabled}
        '''
        result = self._values.get("snowplow_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sourcegraph_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Sourcegraph integration. If enabled, requires sourcegraph_url.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sourcegraph_enabled ApplicationSettings#sourcegraph_enabled}
        '''
        result = self._values.get("sourcegraph_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sourcegraph_public_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Blocks Sourcegraph from being loaded on private and internal projects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sourcegraph_public_only ApplicationSettings#sourcegraph_public_only}
        '''
        result = self._values.get("sourcegraph_public_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sourcegraph_url(self) -> typing.Optional[builtins.str]:
        '''The Sourcegraph instance URL for integration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#sourcegraph_url ApplicationSettings#sourcegraph_url}
        '''
        result = self._values.get("sourcegraph_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spam_check_api_key(self) -> typing.Optional[builtins.str]:
        '''API key used by GitLab for accessing the Spam Check service endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#spam_check_api_key ApplicationSettings#spam_check_api_key}
        '''
        result = self._values.get("spam_check_api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spam_check_endpoint_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables spam checking using external Spam Check API endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#spam_check_endpoint_enabled ApplicationSettings#spam_check_endpoint_enabled}
        '''
        result = self._values.get("spam_check_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def spam_check_endpoint_url(self) -> typing.Optional[builtins.str]:
        '''URL of the external Spamcheck service endpoint.

        Valid URI schemes are grpc or tls. Specifying tls forces communication to be encrypted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#spam_check_endpoint_url ApplicationSettings#spam_check_endpoint_url}
        '''
        result = self._values.get("spam_check_endpoint_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suggest_pipeline_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable pipeline suggestion banner.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#suggest_pipeline_enabled ApplicationSettings#suggest_pipeline_enabled}
        '''
        result = self._values.get("suggest_pipeline_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def terminal_max_session_time(self) -> typing.Optional[jsii.Number]:
        '''Maximum time for web terminal websocket connection (in seconds). Set to 0 for unlimited time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#terminal_max_session_time ApplicationSettings#terminal_max_session_time}
        '''
        result = self._values.get("terminal_max_session_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def terms(self) -> typing.Optional[builtins.str]:
        '''(Required by: enforce_terms) Markdown content for the ToS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#terms ApplicationSettings#terms}
        '''
        result = self._values.get("terms")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def throttle_authenticated_api_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: throttle_authenticated_api_period_in_seconds and throttle_authenticated_api_requests_per_period) Enable authenticated API request rate limit.

        Helps reduce request volume (for example, from crawlers or abusive bots).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_api_enabled ApplicationSettings#throttle_authenticated_api_enabled}
        '''
        result = self._values.get("throttle_authenticated_api_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def throttle_authenticated_api_period_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Rate limit period (in seconds).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_api_period_in_seconds ApplicationSettings#throttle_authenticated_api_period_in_seconds}
        '''
        result = self._values.get("throttle_authenticated_api_period_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttle_authenticated_api_requests_per_period(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Maximum requests per period per user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_api_requests_per_period ApplicationSettings#throttle_authenticated_api_requests_per_period}
        '''
        result = self._values.get("throttle_authenticated_api_requests_per_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttle_authenticated_packages_api_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: throttle_authenticated_packages_api_period_in_seconds and throttle_authenticated_packages_api_requests_per_period) Enable authenticated API request rate limit.

        Helps reduce request volume (for example, from crawlers or abusive bots). View Package Registry rate limits for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_packages_api_enabled ApplicationSettings#throttle_authenticated_packages_api_enabled}
        '''
        result = self._values.get("throttle_authenticated_packages_api_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def throttle_authenticated_packages_api_period_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Rate limit period (in seconds). View Package Registry rate limits for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_packages_api_period_in_seconds ApplicationSettings#throttle_authenticated_packages_api_period_in_seconds}
        '''
        result = self._values.get("throttle_authenticated_packages_api_period_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttle_authenticated_packages_api_requests_per_period(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Maximum requests per period per user. View Package Registry rate limits for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_packages_api_requests_per_period ApplicationSettings#throttle_authenticated_packages_api_requests_per_period}
        '''
        result = self._values.get("throttle_authenticated_packages_api_requests_per_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttle_authenticated_web_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: throttle_authenticated_web_period_in_seconds and throttle_authenticated_web_requests_per_period) Enable authenticated web request rate limit.

        Helps reduce request volume (for example, from crawlers or abusive bots).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_web_enabled ApplicationSettings#throttle_authenticated_web_enabled}
        '''
        result = self._values.get("throttle_authenticated_web_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def throttle_authenticated_web_period_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Rate limit period (in seconds).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_web_period_in_seconds ApplicationSettings#throttle_authenticated_web_period_in_seconds}
        '''
        result = self._values.get("throttle_authenticated_web_period_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttle_authenticated_web_requests_per_period(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Maximum requests per period per user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_authenticated_web_requests_per_period ApplicationSettings#throttle_authenticated_web_requests_per_period}
        '''
        result = self._values.get("throttle_authenticated_web_requests_per_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttle_unauthenticated_api_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: throttle_unauthenticated_api_period_in_seconds and throttle_unauthenticated_api_requests_per_period) Enable unauthenticated API request rate limit.

        Helps reduce request volume (for example, from crawlers or abusive bots).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_api_enabled ApplicationSettings#throttle_unauthenticated_api_enabled}
        '''
        result = self._values.get("throttle_unauthenticated_api_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def throttle_unauthenticated_api_period_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Rate limit period in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_api_period_in_seconds ApplicationSettings#throttle_unauthenticated_api_period_in_seconds}
        '''
        result = self._values.get("throttle_unauthenticated_api_period_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttle_unauthenticated_api_requests_per_period(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Max requests per period per IP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_api_requests_per_period ApplicationSettings#throttle_unauthenticated_api_requests_per_period}
        '''
        result = self._values.get("throttle_unauthenticated_api_requests_per_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttle_unauthenticated_packages_api_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: throttle_unauthenticated_packages_api_period_in_seconds and throttle_unauthenticated_packages_api_requests_per_period) Enable authenticated API request rate limit.

        Helps reduce request volume (for example, from crawlers or abusive bots). View Package Registry rate limits for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_packages_api_enabled ApplicationSettings#throttle_unauthenticated_packages_api_enabled}
        '''
        result = self._values.get("throttle_unauthenticated_packages_api_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def throttle_unauthenticated_packages_api_period_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Rate limit period (in seconds). View Package Registry rate limits for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_packages_api_period_in_seconds ApplicationSettings#throttle_unauthenticated_packages_api_period_in_seconds}
        '''
        result = self._values.get("throttle_unauthenticated_packages_api_period_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttle_unauthenticated_packages_api_requests_per_period(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Maximum requests per period per user. View Package Registry rate limits for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_packages_api_requests_per_period ApplicationSettings#throttle_unauthenticated_packages_api_requests_per_period}
        '''
        result = self._values.get("throttle_unauthenticated_packages_api_requests_per_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttle_unauthenticated_web_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: throttle_unauthenticated_web_period_in_seconds and throttle_unauthenticated_web_requests_per_period) Enable unauthenticated web request rate limit.

        Helps reduce request volume (for example, from crawlers or abusive bots).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_web_enabled ApplicationSettings#throttle_unauthenticated_web_enabled}
        '''
        result = self._values.get("throttle_unauthenticated_web_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def throttle_unauthenticated_web_period_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Rate limit period in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_web_period_in_seconds ApplicationSettings#throttle_unauthenticated_web_period_in_seconds}
        '''
        result = self._values.get("throttle_unauthenticated_web_period_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throttle_unauthenticated_web_requests_per_period(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Max requests per period per IP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#throttle_unauthenticated_web_requests_per_period ApplicationSettings#throttle_unauthenticated_web_requests_per_period}
        '''
        result = self._values.get("throttle_unauthenticated_web_requests_per_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def time_tracking_limit_to_hours(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Limit display of time tracking units to hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#time_tracking_limit_to_hours ApplicationSettings#time_tracking_limit_to_hours}
        '''
        result = self._values.get("time_tracking_limit_to_hours")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def two_factor_grace_period(self) -> typing.Optional[jsii.Number]:
        '''Amount of time (in hours) that users are allowed to skip forced configuration of two-factor authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#two_factor_grace_period ApplicationSettings#two_factor_grace_period}
        '''
        result = self._values.get("two_factor_grace_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unique_ips_limit_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''(If enabled, requires: unique_ips_limit_per_user and unique_ips_limit_time_window) Limit sign in from multiple IPs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#unique_ips_limit_enabled ApplicationSettings#unique_ips_limit_enabled}
        '''
        result = self._values.get("unique_ips_limit_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def unique_ips_limit_per_user(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of IPs per user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#unique_ips_limit_per_user ApplicationSettings#unique_ips_limit_per_user}
        '''
        result = self._values.get("unique_ips_limit_per_user")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unique_ips_limit_time_window(self) -> typing.Optional[jsii.Number]:
        '''How many seconds an IP is counted towards the limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#unique_ips_limit_time_window ApplicationSettings#unique_ips_limit_time_window}
        '''
        result = self._values.get("unique_ips_limit_time_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def usage_ping_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Every week GitLab reports license usage back to GitLab, Inc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#usage_ping_enabled ApplicationSettings#usage_ping_enabled}
        '''
        result = self._values.get("usage_ping_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user_deactivation_emails_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Send an email to users upon account deactivation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_deactivation_emails_enabled ApplicationSettings#user_deactivation_emails_enabled}
        '''
        result = self._values.get("user_deactivation_emails_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user_default_external(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Newly registered users are external by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_default_external ApplicationSettings#user_default_external}
        '''
        result = self._values.get("user_default_external")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user_default_internal_regex(self) -> typing.Optional[builtins.str]:
        '''Specify an email address regex pattern to identify default internal users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_default_internal_regex ApplicationSettings#user_default_internal_regex}
        '''
        result = self._values.get("user_default_internal_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_oauth_applications(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow users to register any application to use GitLab as an OAuth provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_oauth_applications ApplicationSettings#user_oauth_applications}
        '''
        result = self._values.get("user_oauth_applications")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user_show_add_ssh_key_message(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When set to false disable the You won't be able to pull or push project code via SSH warning shown to users with no uploaded SSH key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#user_show_add_ssh_key_message ApplicationSettings#user_show_add_ssh_key_message}
        '''
        result = self._values.get("user_show_add_ssh_key_message")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def version_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Let GitLab inform you when an update is available.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#version_check_enabled ApplicationSettings#version_check_enabled}
        '''
        result = self._values.get("version_check_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def web_ide_clientside_preview_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Live Preview (allow live previews of JavaScript projects in the Web IDE using CodeSandbox Live Preview).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#web_ide_clientside_preview_enabled ApplicationSettings#web_ide_clientside_preview_enabled}
        '''
        result = self._values.get("web_ide_clientside_preview_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def whats_new_variant(self) -> typing.Optional[builtins.str]:
        '''What’s new variant, possible values: all_tiers, current_tier, and disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#whats_new_variant ApplicationSettings#whats_new_variant}
        '''
        result = self._values.get("whats_new_variant")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wiki_page_max_content_bytes(self) -> typing.Optional[jsii.Number]:
        '''Maximum wiki page content size in bytes. The minimum value is 1024 bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/gitlabhq/gitlab/16.3.0/docs/resources/application_settings#wiki_page_max_content_bytes ApplicationSettings#wiki_page_max_content_bytes}
        '''
        result = self._values.get("wiki_page_max_content_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApplicationSettings",
    "ApplicationSettingsConfig",
]

publication.publish()

def _typecheckingstub__75d3980c04bd791033464f1f44824149396aeebc0afa75a6dc4f6952627d2859(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    abuse_notification_email: typing.Optional[builtins.str] = None,
    admin_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    after_sign_out_path: typing.Optional[builtins.str] = None,
    after_sign_up_text: typing.Optional[builtins.str] = None,
    akismet_api_key: typing.Optional[builtins.str] = None,
    akismet_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_group_owners_to_manage_ldap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_local_requests_from_system_hooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_local_requests_from_web_hooks_and_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    archive_builds_in_human_readable: typing.Optional[builtins.str] = None,
    asset_proxy_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    asset_proxy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    asset_proxy_secret_key: typing.Optional[builtins.str] = None,
    asset_proxy_url: typing.Optional[builtins.str] = None,
    authorized_keys_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_devops_domain: typing.Optional[builtins.str] = None,
    auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    automatic_purchased_storage_allocation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    can_create_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    check_namespace_plan: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    commit_email_hostname: typing.Optional[builtins.str] = None,
    container_expiration_policies_enable_historic_entries: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    container_registry_cleanup_tags_service_max_list_size: typing.Optional[jsii.Number] = None,
    container_registry_delete_tags_service_timeout: typing.Optional[jsii.Number] = None,
    container_registry_expiration_policies_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    container_registry_expiration_policies_worker_capacity: typing.Optional[jsii.Number] = None,
    container_registry_token_expire_delay: typing.Optional[jsii.Number] = None,
    deactivate_dormant_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_artifacts_expire_in: typing.Optional[builtins.str] = None,
    default_branch_name: typing.Optional[builtins.str] = None,
    default_branch_protection: typing.Optional[jsii.Number] = None,
    default_ci_config_path: typing.Optional[builtins.str] = None,
    default_group_visibility: typing.Optional[builtins.str] = None,
    default_project_creation: typing.Optional[jsii.Number] = None,
    default_projects_limit: typing.Optional[jsii.Number] = None,
    default_project_visibility: typing.Optional[builtins.str] = None,
    default_snippet_visibility: typing.Optional[builtins.str] = None,
    delayed_group_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delayed_project_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_inactive_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion_adjourned_period: typing.Optional[jsii.Number] = None,
    diff_max_files: typing.Optional[jsii.Number] = None,
    diff_max_lines: typing.Optional[jsii.Number] = None,
    diff_max_patch_bytes: typing.Optional[jsii.Number] = None,
    disabled_oauth_sign_in_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    disable_feed_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dns_rebinding_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    domain_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_denylist: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_denylist_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dsa_key_restriction: typing.Optional[jsii.Number] = None,
    ecdsa_key_restriction: typing.Optional[jsii.Number] = None,
    ecdsa_sk_key_restriction: typing.Optional[jsii.Number] = None,
    ed25519_key_restriction: typing.Optional[jsii.Number] = None,
    ed25519_sk_key_restriction: typing.Optional[jsii.Number] = None,
    eks_access_key_id: typing.Optional[builtins.str] = None,
    eks_account_id: typing.Optional[builtins.str] = None,
    eks_integration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    eks_secret_access_key: typing.Optional[builtins.str] = None,
    elasticsearch_aws: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    elasticsearch_aws_access_key: typing.Optional[builtins.str] = None,
    elasticsearch_aws_region: typing.Optional[builtins.str] = None,
    elasticsearch_aws_secret_access_key: typing.Optional[builtins.str] = None,
    elasticsearch_indexed_field_length_limit: typing.Optional[jsii.Number] = None,
    elasticsearch_indexed_file_size_limit_kb: typing.Optional[jsii.Number] = None,
    elasticsearch_indexing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    elasticsearch_limit_indexing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    elasticsearch_max_bulk_concurrency: typing.Optional[jsii.Number] = None,
    elasticsearch_max_bulk_size_mb: typing.Optional[jsii.Number] = None,
    elasticsearch_namespace_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    elasticsearch_password: typing.Optional[builtins.str] = None,
    elasticsearch_project_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    elasticsearch_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    elasticsearch_url: typing.Optional[typing.Sequence[builtins.str]] = None,
    elasticsearch_username: typing.Optional[builtins.str] = None,
    email_additional_text: typing.Optional[builtins.str] = None,
    email_author_in_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled_git_access_protocol: typing.Optional[builtins.str] = None,
    enforce_namespace_storage_limit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce_terms: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_auth_client_cert: typing.Optional[builtins.str] = None,
    external_auth_client_key: typing.Optional[builtins.str] = None,
    external_auth_client_key_pass: typing.Optional[builtins.str] = None,
    external_authorization_service_default_label: typing.Optional[builtins.str] = None,
    external_authorization_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_authorization_service_timeout: typing.Optional[jsii.Number] = None,
    external_authorization_service_url: typing.Optional[builtins.str] = None,
    external_pipeline_validation_service_timeout: typing.Optional[jsii.Number] = None,
    external_pipeline_validation_service_token: typing.Optional[builtins.str] = None,
    external_pipeline_validation_service_url: typing.Optional[builtins.str] = None,
    file_template_project_id: typing.Optional[jsii.Number] = None,
    first_day_of_week: typing.Optional[jsii.Number] = None,
    geo_node_allowed_ips: typing.Optional[builtins.str] = None,
    geo_status_timeout: typing.Optional[jsii.Number] = None,
    gitaly_timeout_default: typing.Optional[jsii.Number] = None,
    gitaly_timeout_fast: typing.Optional[jsii.Number] = None,
    gitaly_timeout_medium: typing.Optional[jsii.Number] = None,
    git_rate_limit_users_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    git_two_factor_session_expiry: typing.Optional[jsii.Number] = None,
    grafana_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    grafana_url: typing.Optional[builtins.str] = None,
    gravatar_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_owners_can_manage_default_branch_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hashed_storage_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    help_page_hide_commercial_content: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    help_page_support_url: typing.Optional[builtins.str] = None,
    help_page_text: typing.Optional[builtins.str] = None,
    help_text: typing.Optional[builtins.str] = None,
    hide_third_party_offers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    home_page_url: typing.Optional[builtins.str] = None,
    housekeeping_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    housekeeping_full_repack_period: typing.Optional[jsii.Number] = None,
    housekeeping_gc_period: typing.Optional[jsii.Number] = None,
    housekeeping_incremental_repack_period: typing.Optional[jsii.Number] = None,
    html_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    import_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    inactive_projects_delete_after_months: typing.Optional[jsii.Number] = None,
    inactive_projects_min_size_mb: typing.Optional[jsii.Number] = None,
    inactive_projects_send_warning_email_after_months: typing.Optional[jsii.Number] = None,
    in_product_marketing_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    invisible_captcha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issues_create_limit: typing.Optional[jsii.Number] = None,
    keep_latest_artifact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    local_markdown_version: typing.Optional[jsii.Number] = None,
    mailgun_events_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mailgun_signing_key: typing.Optional[builtins.str] = None,
    maintenance_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maintenance_mode_message: typing.Optional[builtins.str] = None,
    max_artifacts_size: typing.Optional[jsii.Number] = None,
    max_attachment_size: typing.Optional[jsii.Number] = None,
    max_export_size: typing.Optional[jsii.Number] = None,
    max_import_size: typing.Optional[jsii.Number] = None,
    max_number_of_repository_downloads: typing.Optional[jsii.Number] = None,
    max_number_of_repository_downloads_within_time_period: typing.Optional[jsii.Number] = None,
    max_pages_size: typing.Optional[jsii.Number] = None,
    max_personal_access_token_lifetime: typing.Optional[jsii.Number] = None,
    max_ssh_key_lifetime: typing.Optional[jsii.Number] = None,
    metrics_method_call_threshold: typing.Optional[jsii.Number] = None,
    mirror_available: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mirror_capacity_threshold: typing.Optional[jsii.Number] = None,
    mirror_max_capacity: typing.Optional[jsii.Number] = None,
    mirror_max_delay: typing.Optional[jsii.Number] = None,
    npm_package_requests_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    outbound_local_requests_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    package_registry_cleanup_policies_worker_capacity: typing.Optional[jsii.Number] = None,
    pages_domain_verification_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_authentication_enabled_for_git: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_authentication_enabled_for_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_lowercase_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_number_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_symbol_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_uppercase_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    performance_bar_allowed_group_path: typing.Optional[builtins.str] = None,
    personal_access_token_prefix: typing.Optional[builtins.str] = None,
    pipeline_limit_per_project_user_sha: typing.Optional[jsii.Number] = None,
    plantuml_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    plantuml_url: typing.Optional[builtins.str] = None,
    polling_interval_multiplier: typing.Optional[jsii.Number] = None,
    project_export_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prometheus_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protected_ci_variables: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    push_event_activities_limit: typing.Optional[jsii.Number] = None,
    push_event_hooks_limit: typing.Optional[jsii.Number] = None,
    pypi_package_requests_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rate_limiting_response_text: typing.Optional[builtins.str] = None,
    raw_blob_request_limit: typing.Optional[jsii.Number] = None,
    recaptcha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recaptcha_private_key: typing.Optional[builtins.str] = None,
    recaptcha_site_key: typing.Optional[builtins.str] = None,
    receive_max_input_size: typing.Optional[jsii.Number] = None,
    repository_checks_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    repository_size_limit: typing.Optional[jsii.Number] = None,
    repository_storages: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_storages_weighted: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
    require_admin_approval_after_user_signup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_two_factor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restricted_visibility_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    rsa_key_restriction: typing.Optional[jsii.Number] = None,
    search_rate_limit: typing.Optional[jsii.Number] = None,
    search_rate_limit_unauthenticated: typing.Optional[jsii.Number] = None,
    send_user_confirmation_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_expire_delay: typing.Optional[jsii.Number] = None,
    shared_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    shared_runners_minutes: typing.Optional[jsii.Number] = None,
    shared_runners_text: typing.Optional[builtins.str] = None,
    sidekiq_job_limiter_compression_threshold_bytes: typing.Optional[jsii.Number] = None,
    sidekiq_job_limiter_limit_bytes: typing.Optional[jsii.Number] = None,
    sidekiq_job_limiter_mode: typing.Optional[builtins.str] = None,
    sign_in_text: typing.Optional[builtins.str] = None,
    signup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    slack_app_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    slack_app_id: typing.Optional[builtins.str] = None,
    slack_app_secret: typing.Optional[builtins.str] = None,
    slack_app_signing_secret: typing.Optional[builtins.str] = None,
    slack_app_verification_token: typing.Optional[builtins.str] = None,
    snippet_size_limit: typing.Optional[jsii.Number] = None,
    snowplow_app_id: typing.Optional[builtins.str] = None,
    snowplow_collector_hostname: typing.Optional[builtins.str] = None,
    snowplow_cookie_domain: typing.Optional[builtins.str] = None,
    snowplow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sourcegraph_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sourcegraph_public_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sourcegraph_url: typing.Optional[builtins.str] = None,
    spam_check_api_key: typing.Optional[builtins.str] = None,
    spam_check_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    spam_check_endpoint_url: typing.Optional[builtins.str] = None,
    suggest_pipeline_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    terminal_max_session_time: typing.Optional[jsii.Number] = None,
    terms: typing.Optional[builtins.str] = None,
    throttle_authenticated_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_authenticated_api_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_authenticated_api_requests_per_period: typing.Optional[jsii.Number] = None,
    throttle_authenticated_packages_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_authenticated_packages_api_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_authenticated_packages_api_requests_per_period: typing.Optional[jsii.Number] = None,
    throttle_authenticated_web_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_authenticated_web_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_authenticated_web_requests_per_period: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_unauthenticated_api_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_api_requests_per_period: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_packages_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_unauthenticated_packages_api_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_packages_api_requests_per_period: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_web_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_unauthenticated_web_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_web_requests_per_period: typing.Optional[jsii.Number] = None,
    time_tracking_limit_to_hours: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    two_factor_grace_period: typing.Optional[jsii.Number] = None,
    unique_ips_limit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unique_ips_limit_per_user: typing.Optional[jsii.Number] = None,
    unique_ips_limit_time_window: typing.Optional[jsii.Number] = None,
    usage_ping_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_deactivation_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_default_external: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_default_internal_regex: typing.Optional[builtins.str] = None,
    user_oauth_applications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_show_add_ssh_key_message: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    version_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    web_ide_clientside_preview_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    whats_new_variant: typing.Optional[builtins.str] = None,
    wiki_page_max_content_bytes: typing.Optional[jsii.Number] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa573503a4f45938a3f93c59d7f2dc99f2f5deeca6c3a3b481a69c809e79d47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195bdec48b52e6d9cfbf4810772fa746527843c488a72772a267544b1978c542(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd567d86cb605da9b8f8548b1f530d80f7b9b9cd0b38ba19e911426fd4095fcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8309494c4a00828fa1f761cc7b34698312e4a70c5471387f09494dcc286ebb34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c83b3b3d12a1ac8bc0ae074c7a6df12b2cf5e11c58b42862f55d3329f6adbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7671322f49949d14cbe4aa247a0db7bf8394eba683800a94540ea2e979e3c80a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84dfaa7453e7b46ad8cb95bf68521a100600ffc077912ffb81ed306d9bbaa21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819a0565a101fa27a608fb45a0b308d41c90d0a3e84f8c78ea9d0ca27d9cb662(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2aad26fd76a2a647c3d1ee056b83a9257767a1a718efb76f2ecc932b7b32b08(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8840f70791cc0b9e9281dee33d281d12575f1be9f937b1baa22328727730ad05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2c495be3de416225fad3461fa21ac39d66e5c6b37d70ae20ed3b47481113e8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4201c1ce37e8e29622940c73df81e184da0d5b62d982bebd4e33e86bac8de472(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e89dce000e7e676512317012419a39595a61882c2d10c94bcdf866e8d56f756(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2abb0f27ff34622f3c92bfc3d0a19d31c62a700eaea15e05c33f919d67c4b89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa10c4f48c41dafd1cd1a507532f123bc24f755720fd297c2d1ac54e7db38da(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31dd3ecf27a4d8ea53ea27142ad327e4a3b461a4cd504410eadb37b8a632ddb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4933d4be0e623aa3573aab3139ec41641a32ca75162eb220114a2ed1609c6f5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592564b8a83472647fe2fdad034afa6dcfb7ed77f51e54a32e4a35858a3f31fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0920b6de4ed161139cd2e3166c42b8ce7d8a3106925c7b962f20653f17784b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf229a4e6dcdd5e58a0eef25b49ed703b33383eab38fc711107f6915a1f6fde6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95fcd57a0126c03d2c97c489ab44087ec1daf0922510e7fcbf022f5b4b65d10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115eb70083b2fc47759c04b000c069744d0900ab2771bb5f36aff7c0af23db8a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfcba578668262e63feef38b4b88f9a43b1ec287e494312dc19fd86e5b87f1fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d925706b4b7e5b1e37085138489f2fda87085a6f36c517a5a22fd739c841b81a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4dec5c9ac39e4f1905d13d66e8fe87a85f27b9e21420adc934a216dfacf71d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__face74d8a7ca04038c27fb02f169d96095e0d392b680eb1acc70ae0a88fd99aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9fec45d9efc0cad487195a512c9017705b2e9411d6770a759afd706f952caee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3997d0de19160dc4bce0c583821e8aa4bc125e0d7353cee051e7ac1ab5b22f78(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2e63ef34bd1aa1b8eabc83598fd2fde267922bb0863008a924843889404290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe776cf51354aadc6cfd18294b7b70cd043221c8ea048f024c5e16b4fafd46b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d640c37b85b9259c231ac41b0fd134145b9e129843b42c7b58d22276dfe92882(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcf51bf08869ed8d0558997d22a4330066e1d184176417ec044f4003ddc57e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770e619f12b4183e97641a142bbcad40a03e5bdf732402299f69270d7bfaa6c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c79695aa028c32f5f07690434c06c42a6f524edc17e76977cedc5fee69056a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3177a573ac67becce30b794704cf25753600eac2ef170bfea5c691dfb62a233d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a18e9f6275354bc8c87be7e188322df5038658b112b3acf227c1ba5870a64b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf54ff5e1f7d8370acaa4bb080109696354c7d4c21bdacbf85b52d14e8bdb02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7b3cdf4d5e99efd8ba11b17c746018783cbf96a6333514dce22d838290c3fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4753a5c192df5e7d748e92ced9cb38c4c476e8bde079c552e700ae4ea6d379f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0375fefb760d2f45930b6562c586e16207418940810b437061feff39741820f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0ece0afbd124e339c95bcb4916833451dcbe7c4cd0152231ddb77ede13dbe3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f9a44022d1b6548bc334d6ae36ec326ee1aac922937a0d831e26c8c0288a0b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a4206909aecdf774bd399b510a5fa7e2cff0cb51c723f6d63fd9ecb7f7be7d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50cc06f90fd4a7badd51e9f60ac48c58fa8af43731bac5068b1e71dccbd97b3f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a778692cf8d526261df878c730ef2966872965488222d43646ca6f8611e569e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a376790bb8980fb468f1e2939bae26fe212184ed8944d6edb2fb5b520f68521(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450598c234758128f504b9961c0ce8c488203822cefb999e53a23754e86afd40(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b50d3c4102ccbad36e4c9b711bb1f9f9768cc8311b38ef88044cebdb7d0996(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ddd96cde6e59c3e7e40a8ef39a4e9ff9aa7689ad0d8e7b27704584206d5a76a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15afdf3d163ea4b5b68f9dd4ca663435f35159b56401972b7d18d31ee70b7105(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab197cbafd4e4b5009ffdf1e1ecbfd420ed7c37b1027cb2cd23e003c47718727(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb025c8b906a15a50054be160d174e05d1c3cc51dc2d1e3da2fddf145e6f1f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705c7d064f8d0fd0dde993fe2dfa25f6eb37b60307730e0e42ebda57cf50152c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552755c563ff21bfc35227644de0d4f14e293501716c97aa6acf86fd83f4ee1c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf8c20f7c66ae2affe14550155718d3b7693de53e84afa9220d278c0ec2b6bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55412fdfe87900505c2561d4b719c3b9eb6c05964d0cc3405eb9c1961ff51df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f30e89051cf0ad9868296cb2009750b06f24cac91c9821549e393cc0a1bc83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387d99cb2c804bbf9d20b6f822c562dfcd58377894b7946a6cc2d3d28f805532(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a712cf93c8611d44d01310729b5eaa8173b5742f78e509da7cffe17c037e091f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65bf35ce107ac03a8aec2608fe67c0e9c13c2f75f92ec64b913d2a0cae4f8407(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5988e85a7db28134cf598d5d5b21322051b897a708afb5c8589bd6b3f411644a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acdde3bda48f94b4f33e28fd2fc4adfaebf5d00e48719eac504c5a79811d88dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5958bfcea1c56e0ee3b7037c1e49ff1f2c4f2f7e4a283f143a795e9d7fb76945(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04ff99674734cfa0337f9172ec4cae02c7618a259e3804dc2550230b46d3452(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c768db788363ed0dd6d8a4d68d0480e0767273ba0081d2e0e3146f99fa78e1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02abe694f0393b81a3d248ee331bde1adef195023a8e81a3842b3b96dd2c911(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b695737f8560b76821d03e56aba40dbb47b0e672dbbb53a1a502031b41d5eef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e33a047821ea4d809285be7c8bc810fcc4e927e19c8f5e5a20f263a6129d514(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c70f0a118a2a498f0371556d5e93c35ccf9b198cbc640362481c73c98aabd9b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ae98cfa0839840b4ad2fe780611f18aab41d42e0d59cf8d5028d34ea4cb949(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e769e82f0cb20b47197bf9df2818e9310775a6917c34c13e8900e4867d681605(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce45bb29b98e15069d4a4bc38b5cac1ee760f62810626b72eccb26ccba96c8cd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44348a62f1cf6bf7200285c5fae5fcecfb15c4f244553b79bc85b36c7b6da2de(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e140a909ccdb09c393ade4e757936c89fdc566e8f42e515d379de9d614fa8235(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de63b347ccf4a9ad2e023151f9f55cf2cbbe76f985197da4bd17e22e65d1732(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c916d7a49303777495f68851d720b3c308dec7b13a0cdccf3f0270737aa8a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e310c42683084bb7d23e7e069d8855f371208fb304a84dca0a92af75a18d209e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787d905ca740f6b5019152939d46c361e29ae1e8fca728fe78e9cfd02eacdca3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fd57d43c0fc614ed129dc54b298490f49716c4a4cd0480b10d7701548a36ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b573a1476cae3f2874b458cb63f2c134f8d938fffe25437e93e1ed149a2744(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6490f0b5a8d251fd84eda6637c2d824bcad132dd843c30458c6fd6eee73afd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330a3fa19856a8601ae5509a92683b91b0ec15a312d64646c934f588df3f2ac0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb56d170ac04bc248dfb8cff82d12d687e76cce8e2b0a1cbdfd5adc347b6aff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18564d64243ad92d1364832c8a5043424c4d81cfd49f47099aa113837e31034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0454f4a03e4fcf0936b4539192aab530c67d6deee47d6bcc11e29c3c0f00e50d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe83534f7fe96ecc9e0db6b169f48a1ed63d5d2aff664213b058112f60bd5c40(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c09b3b061e0e0fd5374c29c4049e7746740c59cb51c86f6320a868c487ad6fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6b8ff1ed4b405e9b419393b014aab2e5cb2af137c4e81fa08b6b5253033245(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d5aeabe8c0c072bca3fe32f580d8f88a004a0064f238ecc574d982210daa8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d969fb2b07b3785bea4f912b48e9b493a6830388184ed5b90f1eb231722822d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8784fe54b256147528d32ddb2c6389566d9cae80b927cd2a94bc283e4007726a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9bc7a29cdb363fd5e46c1ba709c34b001d7c534303df0ce56b2019d9e917cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc01376258c5e7c4df6b4d0fe98ac904cdf73fa424c04fc226edc9283b4f24c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499c824787099b1e6cbdeff5b74450c0fc2fd4917c5edea7ed11e887b8f89433(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a66f7325e4438208961507bf9498e27ad1ae802c70a3f2fea831a0709095645(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48127944d47f172c3b7cee2fc224db36e23e4d50fa6b7d6e07d0ccc71cc4b993(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad53277ccef59b9e7591a3105cef18759bb017c1dcc1bb6e78e14e87d554093(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8166c4efecdb3412ae1322965ac9a16219bf431bbeea984f4cc4240214267bd4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6fae00b4a1da37e525c1f45b494b5cb5284b478c5b9d88f534deec6e0090761(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5964874a644a381707374474460148ed7236f5104f983ee33ea49d20dabbf776(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fced3fc6ceb24294ac04fab81144c96de91917b796143b9d888f4558dc05372c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809394eff63b48adf2c8875c3792c06a6197a2cd8aece30ff78fd4889409bea2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0c67663346c031d82f82718d574041fc9aa1f7f1d403b71cf48979e556215f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c84edcb6476c53c14784c1ad7ee1b4c0775958079d4328352ec22af0ec0f7c63(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e593ec055d08cda6eb2a8d8ee899d1ed63a939ebdca328fd53414e4227ef7a62(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc2a9bdf24b1f22a3d15bcc062431abec9263a0da2f21ff17d67a3dd6805a69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf4048b21a579af2ed5f52791b046e56dd889f549dc04d2a32b98022348545c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1da8f55f6f127d0588f186ce8ef0e4025501cb09b636fa2e273376dc2ee9a1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efeb701b5b439a39622be0aca7ab31fef0316c8bd500b1362b92f2846d7c42c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0201ed2784edea2b985f09770053efab6f583be18ca1b12a123a839fe975274a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95d6aa0795ca71d4ff8fa1e51f13ef40d2ee0855f4159c0165aa6705fa408f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5d20cc9f2714b91d85df4f39c416b3523f98060d2de9cde9bb3486720a510c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69e33710fd6608daef93492bfc94e2e9545c54c8e54f14aa6d03130df19de4e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633463f0acf790baf9dcaef91fb26149c83385d5ed70655354c653b1b51e9439(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbee57fdacdc5368e7e8d7d3d6fd32438bfddaaed7dd00ce3c5144d2d417a8aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a49360754d6cf895e3345343085f9860e5a9636dd9237e304356d6b8889d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ade0be50630d270b560bb453cc433117ae1a4ac477dfd40051e6a823fe84641(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233e1a9116cbf60b4bde135bff521ee4bc63b26e4e090d09a916cf836225f887(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce8761e77747d51ca1dd7938ff5851739a336801a6bf6b79b2dbc178db22ed2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e05afad5201e034086d5a533073271d3875a4a7e14849ceef2ba977e3be7fc9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51e7362b701e82645b4676f0c507e9c3aa0fee7a48cfa4fad0e7ed03b86e0e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b86e1030c11cfe22d5e5a9762872e77f401dff953f25495f321cc84ffebde6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1466c48781cd7981dc59a6a4d5b777161dfd2d23db5daa55c606865678b7a4b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__280eed4e3e860523a535f85509b7015d776d64906b67422d1d4d0bef2f5c624c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ab352eae928e05a96c1ebdb6758bd408ceee399e1d8cacaf083bd51d9ad592(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c928949d2d694927da29424c7060ff39687b894033c5e4b46a30bf1010d540(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e581dbaa2aa7c15b20414962cedacbd64d7a3f67e70c851b45da5e3d444e477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff23cccbb7342bfffd0f76dc590f30ea77e9efc93135ee8090b22d40161daf64(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c43a8656427a874d37c72f8ec75a6c6c2f8a0cc204e1c53e5f363fc992237c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d633ee1fcf7403108b14df4f8aa90c895549d1165d0a554c400c5f90d2250d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bef462704cf1877a2d4e9873724ea79d6dc9e68c61bd4c999bc1311eb56395e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a0a140ac67114e5287a31cd4f63056d3591cd8baa6d3a6a1880b115de1a61e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3436060588fc35e237d78eea35a1ff75bbef64667f28c9c2f83a42ab14613ecf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e483dc8bd5b2b30950be8b6cbed4e90fa7c6cd46498f87976cde39c58a94441c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f42d43c863bb180a8f7703965859bf6aa10088437a1af8faad4e552b8fd38c3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022d9760ba4f8bbff894732c80ab690d64fb08d132d0c59349b1537bce595f67(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbeae9e2d398e54634c5dd753121c04ecb9c4e80034408439454e1f320a40072(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c7c11f12d1386c042ff21f0b6eb6d849cbafc0a1de6894992b15feeec65203(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5890cb97900107e7449e805c7ebbb801080218a9cd20691ed8d7080e6c42feaa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6f0e3d591514f3b17ccd956a7bad812afd504c9f14aebc4b0e62c5522c5d48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b0a0d8d07f884b647e68711ee77b64421d870ffe53819a33cef4c6da32eb61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10daf1a08ba773ad94f112d86d5f2cbdaef84e1922def74f1516f79259d2ed16(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4982493e67f9f4073fe2ce75e3559ea0272cced56f0caf2e0ca2f2b9c4cbe3f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0fe443163b5f619da39990b705583f71202674a40f17c1268c3aabf14172d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3257bed68a1b35232d7b1713f648d4ccb2f20e6ff92e8b0da92418f493fc84(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a253defc20a7d050ae889ba8b6b367bc3e668c16916fba48bd1c506d52dedd31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac07ff1e54d83f7985a327525dc69be6800e7b45c3fb004f161a922bfe17be91(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0376e5766ce583312bff595c953665200e534c967ddedbe8c06861b965a4e290(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571ec836c876cd5c029ec61d9382428136763fd9fa3592d6c1da5bb38ca6d658(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289f13380b64aff9610a79a6c90becd7a22cf64247a314d0b618aef759b56082(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec6c9be6e12370cc63fd6d468b21e619e03704bf4429e374e4759a9919eb3cab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2dfbd350eebc8bf4637d428856bc50cd4ebc6e7238dbeff086e4f389a3b5b4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fed18e1fba5fc202a0b461a80ed32a7539382ca90bf1cfaff63041788ae4cdb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c22478ec8dfc35d8e9ed9a35893ab9a6d060a5a2e933eda14bfe6c423b9482(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754068b55498b76cc1ea5c64d92b3243346e713f99bcabe4fe538eeec99bb28b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397dbe39991fd386b30e675a8ba7dc1213bf27c52d9f94d0c22bcad6908ea225(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01244d310e63cc77c7f6dacdfc901fd703d91685d588be8bda639db634d1bcd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed3afcbf0b1612e2255524a417babf2d3a058331b3961cc87564b1bf67d1279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c548f2c0808730f9d1c62de700bb9ef294ee4b579e7d30c33cbd8fd520a0581(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13836813f19f67abfef06f04d62d327bd4249448df02d713a3990c8fd72aa69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0751641429446f7f7669472813a3bea8cfe5cfe53b2491b204bd6bee26834ead(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15dcb7261c894ca4361571f53196f7d93489f8026ba918e56f7a6aca99dd08d1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2615da62324d55a672c129966772980d62a9b5f66fc98ada3a11f53818a001e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd1b7b1ffb39eb2f2b3c6e444275c94cbf8b890883af5b83fd5e2c0c42ceacb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6bf5a5bf6b2ecb3e8bd3bc7c68fb56528dac9f68c689ab2f2189efdeac3d76e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f3ef6650c38d975c9bcb43ae9ffff8af8131885395f4917a4f4f081a74e917(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1957233ea41acd5835f1572354ac68b030b8df483b733b36ac61c9c71178839a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102ecb9e503e6226387700430566413e3471bde5dc66cf0a9241af5d3a7c2fe4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e6b1146b6a969011e371c7f94fa794adcdbe4137bdaa61330ce9adbd9945ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9c844bae03ec16295641d26c30f99e682bacd7c3e00451a750310b5ec36fe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc893e0d8697bb32a6017c3ebee75048b7544721676c58f84c05ec92f106acb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722ab4d7375476bb665ad8e39ad584aefe8aa712243a3d050bd9ede18e63d6f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacce962f8ea17c3c9608f484b36ddaef1d21739cb7b703edb9adcf2962a52b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a79f5f10f31808431b8b3c2a8a3764a980d2d19cd069189fa821fcbbc0d6ed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff93a7f9f26ca7253f860d2e7ad9cf0d3b58e8aba63689dd68ba267692108eb8(
    value: typing.Mapping[builtins.str, jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd213053e802470cbecc9cf0ce5fc7b35e57ad59ddd86fe91f9fbc2485dcf02c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79792c861918a68c7aac824e823ca2602d6859da06e7df5b6c83e1e4accc8da(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014984cca0761fbbce824e98cbbb8f6210797a90e5f46374567236617088bf15(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4b2fc48459271dc56f752cc5c78f5306b6ab09939eaaea57e7b7dbde5ed7f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c169921079c0f1c59af846856152c006e026e89c5f7aae8dfed277b7cd02534(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06efac3a61ad810ebc4aec4fcac75b711ea8df46a2668beb87cfe60a56581ba8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67837aa9f2abff375171fbdf1087ec883870dea0960a890a35c92c8088614435(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771a3286fb612560296eb9c2efdd6a8fdf77250aaa15df43858da1f9a842abc4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b3116108d005bc6e5880187e50fa9cae3887bf1637dd6dd57494cf83048427(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ad226c5e99504a3e392445987b6d6d59c6c2888aa165ecbbc5d89a4cdb09a5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5203e60f339316ae4573936bc9aee3c436f4cf9da8412c4f6ab61211bf0e18e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b0b8099beb4432e50c55fd90deb894ad4305ecf7714ea7a239e700219bc7e9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1ca2d9c3d39684eeb3d250cdf1ba7f2fc4c36762699f155800d1d4e09966f7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db959f5ec543832e64571b6b4619b12915a89d9d34b0d7d1247ad74ecdf0c5a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0c7d6e6e860f60cf83df049d15bcd503ece0fc317960cc8d4712932b634caf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0643bdc5370f67d2fd0ec9035c2c2170a4a4dce7095e547d740f4e653d73e1e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774b00ffc67699a5f0aa73fc3b9c4b3051dfedcde18dfa7354486510d7d3cf59(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aafbb6b78303ce93be9a4b2342895cbc6d72064f7ef26700d3770b82ebee4be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0976d4ca51430c2d725e9ef14468ce4f445bb004f2fe8a3709d65f7a6eb3cea6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5d883d2a275d7bc3cc32fff6bd7adadaae3856f9f0e1cdea80948a94fdb323(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c217021cb03104cc9e5cf6c833f107032af3d5d563e072de7cff033e40cdef14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0105f8e7dde004cfd8d916dc6dcf3d23b8d86103fb773257f41d563c8346d0da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7cc9c17fceac4b950fb7a12eb3a767410aafc8c6582e1d8cd137cd2b60d6561(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36503f45aec174140294ae242f02907800a8a50a1842fe136876e0a63a9d8fc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b4cab95c74923759ea4cdd0d3b1550ff57db433a7bbe61da02f7db984d0803(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4529d7caa366c1c495fce7b7f92065f4dce0340b098f0a776e156c848c0f8def(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc71d65f9c6a71afad5c454c8b9ab62e4c2edef76aecbb3d83acce365389b15(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821e13884cb3f294d531fceb12e8bf261bb3b16226e74d725b24e71f7ebfd231(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2dd3fe47585e5638ab00f2dab5c2f89165f7b9aa8959a77e88cbfe77191101d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809b9ada1e16fab6e8130aa10c8d2d42e708ff5ac43df6ffde8e67ebe33d05bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db02870aa00bc04b0202077056377d300634891740064930d0dc8f51fd1d2bf1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4a7d16b71eccf9d9d03851fbeaf650163337c5047a8bbe061766ad19442147(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4040207b681d5aadf6f3a9ad41a57cb84d4c33591cb391d53591b884a6d5e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a099e532cafade9f1107acab326529d50151dba85cc0892cf32634b3ec0717(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc49516b8fe9e35a916659f708ef0c19cc68dbc36d00391f2d0f9c9596dda709(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7f170397d65a92ca24a6a5d14adc2956da08161bce7d7f655808e5b9899f74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a99dc518c5bc8a646f005b95a2250d72b88ae61c2387d0c075925209be5ca1e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98003193344171b455bd8dca3e3bfd8aa76a536914de3c94274081ea200e63fb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363bd5d55745915c8ad758f8f23c449d0db75eb3d008d813dd3354455eac288f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4141e09107fc67128670f0f4caaf75a71f76100eb77dd6fafb4a98e583c39d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb41bdd1b3c2fead2e4556e32f000447efcf37c89cee503648639a509ae0266(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d82949e4417f718fe69516c47a4be60ffeab7f12016ef3562a824a559c2f1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65128c503945a5bc2c599f1d4cbc81113e3aa6b1f6f656bdb20495f04c7ae29a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c727224210e2010a9829f9876009406b87c758cda74545dfaa727f42299588(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63935ce53157de1993e608c3ab25b06f0df5269839cc1753e9c421b90b4459e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a636881d648ce07d1875163a672d3a3d52c1588087acb699f89a2b5ba85e23e3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2013017adcaf76b68d9e8b4e0b90e96e84071b4abf4eb152c07288c833f93791(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881bd1528d14845f681f6d27e071252c72f9cd9ec4337ba63ea97e9e223cbef9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ac867a5a84551164b17dbf2723ec471496fdf01fe3622011ae485a7d8ff3e3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae50d1553a6acceb9b0cb3ce7a649dc8a7539ec3c0205b120ebefb399e33fd1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948de55c1e4c2b951947365d1cd59dc7d9eab1249f65b20e398414df0982f1bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4978b08f915757d709ad4ef7b9bc73fc425419c94f001606c6fdb2af4b95e513(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e636a9a0b817a43fa0f39c2469e57eeb627716e0031fa640bd4b65a5c3c607(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6203d46a2aff03f6781334a47a98c5f345e8cd4e4ff1b9023a789988750e72(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2889d24f1c18a31ded8d26772d11c7d2070629cef13072a357bfe0d0d7210dbf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810b9dda6f58abf0039a94974810b81e552631a1bdd36e3ca5525b75c1276b5c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe0650128f4cf780f0a2915b1e32445ee8696b19ea0fa7f9b51657723d7afcc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0c4554cc41b227b1cd23ede4f55271c0e38435759587e6f9f7dce381b39228(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248d53078b8907c6120b1a0e8fc1c128b74d48f5d13a6f3aa0d06df7272cec7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5526514a99981349d177fa6f57768f803c82234f9c1eea2a6eabc05521f3fae7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd7206d25baff569e6348a26a5c0fc760ce42a20f47e354e018af57f0552981(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7d15f089aa9d346a6458f91e2fbc568da255334df9f1d83c9b80f973d17c15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7668c25cdb8cd238202f05d6917384eea1f38391fcae1c6c400803854c3b165f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffdcecbaa9bb071ba18049e109dbd21b1ea75a25bb530afb7f4e38e5b37454c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c26da11252c881468bd451a23577f6762ffd24c5e6344c7dc9e3569649532ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28320ae7a9b4b14eb48b6bd7175269fd6cc51ad33df62db9ac38717d53636d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03a40b699ab248d4fc8ba417d6c1d7e350c29cb494a4c594cfd6cd401e36dad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7f961fa567c203b84eb5b0fbfa3e065a5025582305a3b108bfa2fa7f002f4c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50b86976e6a321d315529ec7b5d8fe1bc23f479e146940bc53976f68530f641(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    abuse_notification_email: typing.Optional[builtins.str] = None,
    admin_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    after_sign_out_path: typing.Optional[builtins.str] = None,
    after_sign_up_text: typing.Optional[builtins.str] = None,
    akismet_api_key: typing.Optional[builtins.str] = None,
    akismet_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_group_owners_to_manage_ldap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_local_requests_from_system_hooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_local_requests_from_web_hooks_and_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    archive_builds_in_human_readable: typing.Optional[builtins.str] = None,
    asset_proxy_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    asset_proxy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    asset_proxy_secret_key: typing.Optional[builtins.str] = None,
    asset_proxy_url: typing.Optional[builtins.str] = None,
    authorized_keys_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_devops_domain: typing.Optional[builtins.str] = None,
    auto_devops_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    automatic_purchased_storage_allocation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    can_create_group: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    check_namespace_plan: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    commit_email_hostname: typing.Optional[builtins.str] = None,
    container_expiration_policies_enable_historic_entries: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    container_registry_cleanup_tags_service_max_list_size: typing.Optional[jsii.Number] = None,
    container_registry_delete_tags_service_timeout: typing.Optional[jsii.Number] = None,
    container_registry_expiration_policies_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    container_registry_expiration_policies_worker_capacity: typing.Optional[jsii.Number] = None,
    container_registry_token_expire_delay: typing.Optional[jsii.Number] = None,
    deactivate_dormant_users: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_artifacts_expire_in: typing.Optional[builtins.str] = None,
    default_branch_name: typing.Optional[builtins.str] = None,
    default_branch_protection: typing.Optional[jsii.Number] = None,
    default_ci_config_path: typing.Optional[builtins.str] = None,
    default_group_visibility: typing.Optional[builtins.str] = None,
    default_project_creation: typing.Optional[jsii.Number] = None,
    default_projects_limit: typing.Optional[jsii.Number] = None,
    default_project_visibility: typing.Optional[builtins.str] = None,
    default_snippet_visibility: typing.Optional[builtins.str] = None,
    delayed_group_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delayed_project_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_inactive_projects: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion_adjourned_period: typing.Optional[jsii.Number] = None,
    diff_max_files: typing.Optional[jsii.Number] = None,
    diff_max_lines: typing.Optional[jsii.Number] = None,
    diff_max_patch_bytes: typing.Optional[jsii.Number] = None,
    disabled_oauth_sign_in_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    disable_feed_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dns_rebinding_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    domain_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_denylist: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_denylist_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dsa_key_restriction: typing.Optional[jsii.Number] = None,
    ecdsa_key_restriction: typing.Optional[jsii.Number] = None,
    ecdsa_sk_key_restriction: typing.Optional[jsii.Number] = None,
    ed25519_key_restriction: typing.Optional[jsii.Number] = None,
    ed25519_sk_key_restriction: typing.Optional[jsii.Number] = None,
    eks_access_key_id: typing.Optional[builtins.str] = None,
    eks_account_id: typing.Optional[builtins.str] = None,
    eks_integration_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    eks_secret_access_key: typing.Optional[builtins.str] = None,
    elasticsearch_aws: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    elasticsearch_aws_access_key: typing.Optional[builtins.str] = None,
    elasticsearch_aws_region: typing.Optional[builtins.str] = None,
    elasticsearch_aws_secret_access_key: typing.Optional[builtins.str] = None,
    elasticsearch_indexed_field_length_limit: typing.Optional[jsii.Number] = None,
    elasticsearch_indexed_file_size_limit_kb: typing.Optional[jsii.Number] = None,
    elasticsearch_indexing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    elasticsearch_limit_indexing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    elasticsearch_max_bulk_concurrency: typing.Optional[jsii.Number] = None,
    elasticsearch_max_bulk_size_mb: typing.Optional[jsii.Number] = None,
    elasticsearch_namespace_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    elasticsearch_password: typing.Optional[builtins.str] = None,
    elasticsearch_project_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    elasticsearch_search: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    elasticsearch_url: typing.Optional[typing.Sequence[builtins.str]] = None,
    elasticsearch_username: typing.Optional[builtins.str] = None,
    email_additional_text: typing.Optional[builtins.str] = None,
    email_author_in_body: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enabled_git_access_protocol: typing.Optional[builtins.str] = None,
    enforce_namespace_storage_limit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce_terms: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_auth_client_cert: typing.Optional[builtins.str] = None,
    external_auth_client_key: typing.Optional[builtins.str] = None,
    external_auth_client_key_pass: typing.Optional[builtins.str] = None,
    external_authorization_service_default_label: typing.Optional[builtins.str] = None,
    external_authorization_service_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_authorization_service_timeout: typing.Optional[jsii.Number] = None,
    external_authorization_service_url: typing.Optional[builtins.str] = None,
    external_pipeline_validation_service_timeout: typing.Optional[jsii.Number] = None,
    external_pipeline_validation_service_token: typing.Optional[builtins.str] = None,
    external_pipeline_validation_service_url: typing.Optional[builtins.str] = None,
    file_template_project_id: typing.Optional[jsii.Number] = None,
    first_day_of_week: typing.Optional[jsii.Number] = None,
    geo_node_allowed_ips: typing.Optional[builtins.str] = None,
    geo_status_timeout: typing.Optional[jsii.Number] = None,
    gitaly_timeout_default: typing.Optional[jsii.Number] = None,
    gitaly_timeout_fast: typing.Optional[jsii.Number] = None,
    gitaly_timeout_medium: typing.Optional[jsii.Number] = None,
    git_rate_limit_users_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    git_two_factor_session_expiry: typing.Optional[jsii.Number] = None,
    grafana_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    grafana_url: typing.Optional[builtins.str] = None,
    gravatar_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    group_owners_can_manage_default_branch_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hashed_storage_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    help_page_hide_commercial_content: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    help_page_support_url: typing.Optional[builtins.str] = None,
    help_page_text: typing.Optional[builtins.str] = None,
    help_text: typing.Optional[builtins.str] = None,
    hide_third_party_offers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    home_page_url: typing.Optional[builtins.str] = None,
    housekeeping_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    housekeeping_full_repack_period: typing.Optional[jsii.Number] = None,
    housekeeping_gc_period: typing.Optional[jsii.Number] = None,
    housekeeping_incremental_repack_period: typing.Optional[jsii.Number] = None,
    html_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    import_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    inactive_projects_delete_after_months: typing.Optional[jsii.Number] = None,
    inactive_projects_min_size_mb: typing.Optional[jsii.Number] = None,
    inactive_projects_send_warning_email_after_months: typing.Optional[jsii.Number] = None,
    in_product_marketing_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    invisible_captcha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    issues_create_limit: typing.Optional[jsii.Number] = None,
    keep_latest_artifact: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    local_markdown_version: typing.Optional[jsii.Number] = None,
    mailgun_events_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mailgun_signing_key: typing.Optional[builtins.str] = None,
    maintenance_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    maintenance_mode_message: typing.Optional[builtins.str] = None,
    max_artifacts_size: typing.Optional[jsii.Number] = None,
    max_attachment_size: typing.Optional[jsii.Number] = None,
    max_export_size: typing.Optional[jsii.Number] = None,
    max_import_size: typing.Optional[jsii.Number] = None,
    max_number_of_repository_downloads: typing.Optional[jsii.Number] = None,
    max_number_of_repository_downloads_within_time_period: typing.Optional[jsii.Number] = None,
    max_pages_size: typing.Optional[jsii.Number] = None,
    max_personal_access_token_lifetime: typing.Optional[jsii.Number] = None,
    max_ssh_key_lifetime: typing.Optional[jsii.Number] = None,
    metrics_method_call_threshold: typing.Optional[jsii.Number] = None,
    mirror_available: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mirror_capacity_threshold: typing.Optional[jsii.Number] = None,
    mirror_max_capacity: typing.Optional[jsii.Number] = None,
    mirror_max_delay: typing.Optional[jsii.Number] = None,
    npm_package_requests_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    outbound_local_requests_whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    package_registry_cleanup_policies_worker_capacity: typing.Optional[jsii.Number] = None,
    pages_domain_verification_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_authentication_enabled_for_git: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_authentication_enabled_for_web: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_lowercase_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_number_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_symbol_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_uppercase_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    performance_bar_allowed_group_path: typing.Optional[builtins.str] = None,
    personal_access_token_prefix: typing.Optional[builtins.str] = None,
    pipeline_limit_per_project_user_sha: typing.Optional[jsii.Number] = None,
    plantuml_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    plantuml_url: typing.Optional[builtins.str] = None,
    polling_interval_multiplier: typing.Optional[jsii.Number] = None,
    project_export_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prometheus_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    protected_ci_variables: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    push_event_activities_limit: typing.Optional[jsii.Number] = None,
    push_event_hooks_limit: typing.Optional[jsii.Number] = None,
    pypi_package_requests_forwarding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rate_limiting_response_text: typing.Optional[builtins.str] = None,
    raw_blob_request_limit: typing.Optional[jsii.Number] = None,
    recaptcha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recaptcha_private_key: typing.Optional[builtins.str] = None,
    recaptcha_site_key: typing.Optional[builtins.str] = None,
    receive_max_input_size: typing.Optional[jsii.Number] = None,
    repository_checks_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    repository_size_limit: typing.Optional[jsii.Number] = None,
    repository_storages: typing.Optional[typing.Sequence[builtins.str]] = None,
    repository_storages_weighted: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
    require_admin_approval_after_user_signup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_two_factor_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restricted_visibility_levels: typing.Optional[typing.Sequence[builtins.str]] = None,
    rsa_key_restriction: typing.Optional[jsii.Number] = None,
    search_rate_limit: typing.Optional[jsii.Number] = None,
    search_rate_limit_unauthenticated: typing.Optional[jsii.Number] = None,
    send_user_confirmation_email: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    session_expire_delay: typing.Optional[jsii.Number] = None,
    shared_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    shared_runners_minutes: typing.Optional[jsii.Number] = None,
    shared_runners_text: typing.Optional[builtins.str] = None,
    sidekiq_job_limiter_compression_threshold_bytes: typing.Optional[jsii.Number] = None,
    sidekiq_job_limiter_limit_bytes: typing.Optional[jsii.Number] = None,
    sidekiq_job_limiter_mode: typing.Optional[builtins.str] = None,
    sign_in_text: typing.Optional[builtins.str] = None,
    signup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    slack_app_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    slack_app_id: typing.Optional[builtins.str] = None,
    slack_app_secret: typing.Optional[builtins.str] = None,
    slack_app_signing_secret: typing.Optional[builtins.str] = None,
    slack_app_verification_token: typing.Optional[builtins.str] = None,
    snippet_size_limit: typing.Optional[jsii.Number] = None,
    snowplow_app_id: typing.Optional[builtins.str] = None,
    snowplow_collector_hostname: typing.Optional[builtins.str] = None,
    snowplow_cookie_domain: typing.Optional[builtins.str] = None,
    snowplow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sourcegraph_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sourcegraph_public_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sourcegraph_url: typing.Optional[builtins.str] = None,
    spam_check_api_key: typing.Optional[builtins.str] = None,
    spam_check_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    spam_check_endpoint_url: typing.Optional[builtins.str] = None,
    suggest_pipeline_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    terminal_max_session_time: typing.Optional[jsii.Number] = None,
    terms: typing.Optional[builtins.str] = None,
    throttle_authenticated_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_authenticated_api_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_authenticated_api_requests_per_period: typing.Optional[jsii.Number] = None,
    throttle_authenticated_packages_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_authenticated_packages_api_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_authenticated_packages_api_requests_per_period: typing.Optional[jsii.Number] = None,
    throttle_authenticated_web_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_authenticated_web_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_authenticated_web_requests_per_period: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_unauthenticated_api_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_api_requests_per_period: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_packages_api_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_unauthenticated_packages_api_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_packages_api_requests_per_period: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_web_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    throttle_unauthenticated_web_period_in_seconds: typing.Optional[jsii.Number] = None,
    throttle_unauthenticated_web_requests_per_period: typing.Optional[jsii.Number] = None,
    time_tracking_limit_to_hours: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    two_factor_grace_period: typing.Optional[jsii.Number] = None,
    unique_ips_limit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unique_ips_limit_per_user: typing.Optional[jsii.Number] = None,
    unique_ips_limit_time_window: typing.Optional[jsii.Number] = None,
    usage_ping_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_deactivation_emails_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_default_external: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_default_internal_regex: typing.Optional[builtins.str] = None,
    user_oauth_applications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_show_add_ssh_key_message: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    version_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    web_ide_clientside_preview_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    whats_new_variant: typing.Optional[builtins.str] = None,
    wiki_page_max_content_bytes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
