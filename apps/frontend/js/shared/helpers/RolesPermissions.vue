<script>
export default {
    name: "RolesPermissions",
    methods: {
        hasRole(role) {
            if (!this.$page.props.auth || !role) { return false }
            let userRoles = this.$page.props.auth.roles;
            let roles = role.split("|");
            for (let i = 0; i < roles.length; i++) {
                if (userRoles.includes(roles[i])) { return true }
            }
            return false
        },
        roles() {
          return this.$page.props.auth.roles
        },
        permissions() {
            return this.$page.props.auth.permissions
        },
        device_type() {
            return this.$page.props.device_type
        },
        can(permission) {
            if (!this.$page.props.auth || !permission) { return false }
            let userPermissions = this.$page.props.auth.permissions;
            let permissions = permission.split("|");
            for (let i = 0; i < permissions.length; i++) {
                if (userPermissions.includes(permissions[i])) { return true }
            }
            return false
        }
    }
}
</script>
