# wfmr-bitbar
A [BitBar](https://github.com/matryer/bitbar) plugin to track [Wells Fargo's mortgage interest rates](https://www.wellsfargo.com/mortgage/rates/) and sends you a txt notification with Twilio. Currently, the plugin is only tracking [Wells Fargo 30 year fixed rate confirming purchase loan interest rate](https://www.wellsfargo.com/mortgage/rates/purchase-assumptions?prod=1).

# Setup
1. Clone the repo into your BitBar Plugins folder
2. Create an account on [Twilio](https://twilio.com/console/)
3. Create a project on Twilio
4. Verify your phone number under your Account Settings
5. Generate the `ACCOUNT SID` and `AUTH TOKEN` for your project
6. Add a phone number to your project
7. Paste all that data from previous steps under the `SETUP` section in `wmfr-tracker/interest-rate-checker.py`
8. `chmod +x wfmr-tracker.10m.sh`
