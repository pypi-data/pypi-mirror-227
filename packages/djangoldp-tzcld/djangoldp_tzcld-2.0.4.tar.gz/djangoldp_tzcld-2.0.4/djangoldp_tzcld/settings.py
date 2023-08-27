COMMUNITY_NESTED_FIELDS = ['tzcld_profile', 'tzcld_profile_identity']
COMMUNITY_ADMIN_INLINES = [("djangoldp_tzcld.admin", "TzcldCommunityInline",)]
USER_NESTED_FIELDS = ['tzcld_profile']