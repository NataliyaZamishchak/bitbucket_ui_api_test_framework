from playwright.sync_api import Locator, expect
from utils.logger import get_logger

logger = get_logger(__name__)

class UsersPermissionsTable:
    """Represents the user permissions table."""

    def __init__(self, root_locator: Locator):
        """Initialize the user permissions table."""
        self.root = root_locator
        self.rows = self.root.locator("tbody tr")

    def get_row_by_username(self, username: str) -> Locator | None:
        """Get a table row by username."""
        logger.info(f"Searching for row with username: {username}")
        row_count = self.rows.count()
        for i in range(row_count):
            row = self.rows.nth(i)
            name_cell = row.locator("td").nth(1)
            if name_cell.locator("a").is_visible():
                name = name_cell.locator("a").inner_text().strip()
            else:
                name = name_cell.locator("span").nth(1).inner_text().strip()
            if name == username:
                logger.info(f"Found row for username: {username}")
                return row
        logger.warning(f"Row for username '{username}' not found")
        return None

    def get_user_row_data(self, username: str) -> dict | None:
        """Get user row data as a dictionary."""
        row = self.get_row_by_username(username)
        if not row:
            logger.warning(f"No data found for username: {username}")
            return None
        return {
            "Name": row.locator("td").nth(1).locator('span').nth(1).inner_text().strip(),
            "Permission": row.locator("td").nth(2).locator('button span').nth(0).inner_text().strip(),
            "Access level": row.locator("td").nth(3).inner_text().strip(),
            "Actions": row.locator("td").nth(4).locator('button span').inner_text().strip(),
        }

    def get_permission_cell(self, row: Locator) -> Locator:
        """Get the permission cell for a row."""
        return row.locator("td").nth(2)

    def get_actions_cell(self, row: Locator) -> Locator:
        """Get the actions cell for a row."""
        return row.locator("td").nth(4)

    def get_dropdown(self) -> Locator:
        """Get the permissions dropdown."""
        return self.root.page.locator('[data-testid="privilegesDropdown--content"]')

    def get_permission_button_for_row(self, row: Locator):
        """Get the permission button for a row."""
        return self.get_permission_cell(row).locator('[data-testid="privilegesDropdown--trigger"]')

    def get_actions_button_for_row(self, row: Locator):
        """Get the actions button for a row."""
        return self.get_actions_cell(row).locator('button')

    def get_dropdown_option(self, permission: str) -> Locator:
        """Get a dropdown option by permission name."""
        return self.get_dropdown().locator(
            f'//button[@role="menuitem"][.//span[text()="{permission}"]]'
        )

    def set_user_permission(self, username: str, new_permission: str):
        """Set a new permission for a user."""
        logger.info(f"Setting permission '{new_permission}' for user: {username}")
        row = self.get_row_by_username(username)
        if not row:
            logger.error(f"User '{username}' not found in table")
            raise ValueError(f"User '{username}' not found in table")

        self.get_permission_cell(row).click()
        self.get_dropdown().wait_for(state="visible")
        self.get_dropdown_option(new_permission).click()
        row = self.get_row_by_username(username)
        expect(self.get_permission_button_for_row(row)).to_be_enabled(timeout=5000)
        logger.info(f"Permission '{new_permission}' set successfully for user: {username}")

    def click_remove_button(self, username: str):
        """Click the remove button for a user."""
        logger.info(f"Clicking remove button for user: {username}")
        row = self.get_row_by_username(username)
        if not row:
            logger.error(f"User '{username}' not found in table")
            raise ValueError(f"User '{username}' not found in table")
        self.get_actions_button_for_row(row).click()