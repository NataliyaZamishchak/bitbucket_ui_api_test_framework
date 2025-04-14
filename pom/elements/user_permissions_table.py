from playwright.sync_api import Locator, expect


class UsersPermissionsTable:
    def __init__(self, root_locator: Locator):
        self.root = root_locator
        self.rows = self.root.locator("tbody tr")

    def get_row_by_username(self, username: str) -> Locator | None:
        row_count = self.rows.count()
        for i in range(row_count):
            row = self.rows.nth(i)
            name_cell = row.locator("td").nth(1)
            if name_cell.locator("a").is_visible():
                name = name_cell.locator("a").inner_text().strip()
            else:
                name = name_cell.locator("span").nth(1).inner_text().strip()
            if name == username:
                return row
        return None

    def get_user_row_data(self, username: str) -> dict | None:
        row = self.get_row_by_username(username)
        if not row:
            return None
        return {
            "Name": row.locator("td").nth(1).locator('span').nth(1).inner_text().strip(),
            "Permission": row.locator("td").nth(2).locator('button span').nth(0).inner_text().strip(),
            "Access level": row.locator("td").nth(3).inner_text().strip(),
            "Actions": row.locator("td").nth(4).locator('button span').inner_text().strip(),
        }

    def get_permission_cell(self, row: Locator) -> Locator:
        return row.locator("td").nth(2)

    def get_actions_cell(self, row: Locator) -> Locator:
        return row.locator("td").nth(4)

    def get_dropdown(self) -> Locator:
        return self.root.page.locator('[data-testid="privilegesDropdown--content"]')

    def get_permission_button_for_row(self, row: Locator):
        return self.get_permission_cell(row).locator('[data-testid="privilegesDropdown--trigger"]')

    def get_actions_button_for_row(self, row: Locator):
        return self.get_actions_cell(row).locator('button')

    def get_dropdown_option(self, permission: str) -> Locator:
        return self.get_dropdown().locator(
            f'//button[@role="menuitem"][.//span[text()="{permission}"]]'
        )

    def set_user_permission(self, username: str, new_permission: str):
        row = self.get_row_by_username(username)
        if not row:
            raise ValueError(f"User '{username}' not found in table")

        self.get_permission_cell(row).click()
        self.get_dropdown().wait_for(state="visible")
        self.get_dropdown_option(new_permission).click()
        row = self.get_row_by_username(username)
        expect(self.get_permission_button_for_row(row)).to_be_enabled(timeout=5000)

    def click_remove_button(self, username: str):
        row = self.get_row_by_username(username)
        if not row:
            raise ValueError(f"User '{username}' not found in table")
        self.get_actions_button_for_row(row).click()