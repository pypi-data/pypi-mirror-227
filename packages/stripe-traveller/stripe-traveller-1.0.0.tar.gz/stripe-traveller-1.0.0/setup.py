# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stripe_traveller']

package_data = \
{'': ['*']}

install_requires = \
['stripe>=6.1.0,<7.0.0']

setup_kwargs = {
    'name': 'stripe-traveller',
    'version': '1.0.0',
    'description': 'Wraps the Stripe Test Clock object for easier async/await-based test functions.',
    'long_description': "# Stripe Traveller (python)\n\nA significant part of Stripe's functionality is handled via lifecycle events, e.g. an invoice being generated when a subscription reaches the end of its billing cycle. There are two ways to test code that deals with these lifecycle events:\n\n1. Create fixtures that replicate Stripe objects (e.g. `stripe.Subscription`) or events (e.g. `stripe.WebhookEvent`), then pass those fixtures to the end code.\n2. Use Test Clocks to simulate the flow of time in a test environment and allow Stripe to trigger actual lifecycle events.\n\nThe former is great when you need/want to test locally and/or quickly. The latter is great when you want a simpler test framework and want to rely on Stripe to generate objects and events, at the expense of longer test cycles and the inability to receive webhook events locally.\n\nThis library is intended to be used as a test helper for the latter scenario.\n\n## Working with Test Clocks\n\nTest clocks can be difficult to work with directly, in part because you *must* ensure you are disposing of test clocks when your code ends, otherwise you could get stuck with a lot of junk resources in your Stripe test environment.\n\n*Traveller can be used alongside `with` to ensure test clocks are always disposed when the code block is exited.*\n\nAdditionally, test clocks require you to pass in a set point in time to advance to and do not offer relative time advancement functions.\n\n*The `t.advance` function allows for relative time advancement while `t.goto` allows for absolute time advancement.*\n\nFinally, Stripe does not use `async` in their functions, meaning that you must call `clock.advance` and then manually monitor the test clock in a loop while waiting for advancement to complete.\n\n*You can simply `await t.advance` or `await t.goto`.*\n\n## Working with Traveller\n\nThe best way to use the `Traveller` helper class is to use `with Traveller()`.\n\n```python\nwith Traveller() as t:\n    customer = stripe.Customer.create(test_clock=t.clock_id, ...)\n    subscription = stripe.Subscription.create(customer=customer.id, items=items, ..)\n    await t.advance(days=1)\n```\n\nBecause we use `with Traveller()`, we are guaranteed that our test clock will be disposed of no matter how this block termiantes. Whether we fail an `assert`, invoke `exit`, have an uncaught exception, it doesn't matter; `__exit__` will always get called and ensure our test clock is deleted.\n\nAdditionally, we can use relative or absolute time advancement functions via `advance` and `goto`, respectively.\n\nFinally, we can simply `await` either of those functions to ensure that the following lines of code do not execute until the test clock has completed its advancement of time.\n",
    'author': 'Tyler Eon',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
