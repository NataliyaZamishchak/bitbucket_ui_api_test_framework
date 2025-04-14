.PHONY: test report clean

test:
	pytest --alluredir=allure-results

report:
	allure generate allure-results --clean -o allure-report
	allure open allure-report

clean:
	rm -rf allure-results allure-report
