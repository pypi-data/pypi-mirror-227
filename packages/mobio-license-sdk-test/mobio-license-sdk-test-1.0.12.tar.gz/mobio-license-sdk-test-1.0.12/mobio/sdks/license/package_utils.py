from .date_utils import convert_timestamp_to_date_utc, convert_date_to_timestamp, get_utc_now


class PackageUtils:
    class LicenseJson:
        merchant_id = "merchant_id"
        version = "version"
        created_time = "created_time"
        api_key = "api_key"
        alert_merchant = "alert_merchant"
        packages = "packages"

    class LicenseMerchant:
        merchant_id = "merchant_id"
        packages = "packages"
        gift = "gift"
        currency_unit = "currency_unit"
        expire_time = "expire_time"

    class PackageModule:
        cdp = "cdp"
        sales = "sales"
        services = "services"
        all_value = [cdp, sales, services]

    class Package:
        package_code = "package_code"
        module = "module"
        package_type = "package_type"
        attribute_calculate = "attribute_calculate"
        config_calculate = "config_calculate"
        package_parameters = "package_parameters"

        class Attribute:
            allow = "allow"
            attribute_type = "attribute_type"
            max = "max"
            min = "min"

        class AttributeType:
            quantity = "quantity"
            feature = "feature"

    def __init__(self, json_license: dict):
        self.json_license = json_license

    def check_license_module_expired(self, module: str):
        if module not in self.PackageModule.all_value:
            raise ValueError("{} module invalid".format(module))
        module_expire = True
        try:
            expire_time = self.json_license.get(self.LicenseJson.packages, {}).get(
                module, {}).get(self.LicenseMerchant.expire_time, 0)
            if expire_time and convert_timestamp_to_date_utc(expire_time):
                time_stamp_now = convert_date_to_timestamp(get_utc_now())
                if expire_time > time_stamp_now:
                    module_expire = False
                else:
                    print(
                        "license_sdk::check_license_module_expired {} expire_time".format(module)
                    )
            else:
                print(
                    "license_sdk::check_license_module_expired license expire_time not found {}".format(module)
                )
        except Exception as e:
            print("license_sdk::check_license_module_expired: ERROR: %s" % e)
        return module_expire

    def validate_module(self, module: str):
        if module not in self.PackageModule.all_value:
            raise ValueError("{} module invalid".format(module))

    def check_allow_attribute_quantity(self, module: str, attribute: str, number_check: int):
        self.validate_module(module=module)
        is_allowed = False
        try:
            if not self.check_license_module_expired(module=module):
                data_attribute = self.json_license.get(self.LicenseJson.packages, {}).get(
                    module, {}).get(self.LicenseMerchant.packages, {}).get(
                    self.Package.package_parameters, {}).get(attribute, {})
                if (data_attribute and data_attribute.get(self.Package.Attribute.allow) and data_attribute.get(
                        self.Package.Attribute.attribute_type) == self.Package.AttributeType.quantity):
                    number_package = data_attribute.get(self.Package.Attribute.max, 0)
                    if number_package < 0 or number_check <= number_package:
                        is_allowed = True
        except Exception as err:
            print("check_allow_attribute_quantity err: {}".format(err))
        return is_allowed

    def check_allow_attribute_feature(self, module: str, attribute: str):
        self.validate_module(module=module)
        is_allowed = False
        try:
            if not self.check_license_module_expired(module=module):
                data_attribute = self.json_license.get(self.LicenseJson.packages, {}).get(
                    module, {}).get(self.LicenseMerchant.packages, {}).get(
                    self.Package.package_parameters, {}).get(attribute, {})
                if (data_attribute and data_attribute.get(self.Package.Attribute.allow) and data_attribute.get(
                        self.Package.Attribute.attribute_type) == self.Package.AttributeType.feature):
                    is_allowed = True
        except Exception as err:
            print("check_allow_attribute_feature err: {}".format(err))
        return is_allowed


if __name__ == "__main__":
    json_package = {
        "packages": {
            "sales": {
                "packages": {
                    "package_code": "enterprise",
                    "module": "sales",
                    "status": "active",
                    "package_type": "fix",
                    "attribute_calculate": "number_user",
                    "config_calculate": [
                        {
                            'start': 11,
                            'end': 1000,
                            'price': {
                                'vnd': 1_000_000,
                                'usd': 40
                            },
                            'per': 1
                        },
                    ],
                    "price_base": {
                        "vnd": 10_000_000,
                        "usd": 400,
                    },
                    "package_parameters": {
                        "number_user": {
                            "allow": 1,
                            "attribute_type": "quantity",
                            'max': 1000,
                            'min': 10,
                        },
                        "admin_team": {
                            "allow": 1,
                            "attribute_type": "quantity",
                            'max': -1,
                        },
                        "deal_dynamic_field": {
                            "allow": 1,
                            "attribute_type": "quantity",
                            'max': -1,
                        },
                        "media_storage": {
                            "allow": 1,
                            "attribute_type": "quantity",
                            'max': 10,
                        },
                        "deal_pipeline_setup": {
                            "allow": 1,
                            "attribute_type": "quantity",
                            'max': -1,
                        },
                    },
                },
                "expire_time": 2592442000,
            }
        }
    }
    # result = PackageUtils(json_license=json_package).check_allow_attribute_quantity(
    #     module="sales", attribute="number_user", number_check=1001
    # )
    result = PackageUtils(json_license=json_package).check_allow_attribute_feature(
        module="sales", attribute="number_user"
    )
    print(result)