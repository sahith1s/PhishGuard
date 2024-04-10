# PhishGuard

PhishGuard is a security tool designed to detect and prevent phishing attacks by analyzing URLs. It leverages machine learning algorithms to classify URLs as either phishing or legitimate, providing users with real-time protection against malicious websites.

## Features

- Initiate URL verification to check for phishing attempts.
- Validate URL format to ensure proper handling.
- Extract features from URLs for analysis.
- Apply machine learning models to predict the likelihood of phishing.
- Report phishing URLs to the Google Safe Browsing API for further action.

## Installation

To install PhishGuard, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the application using `python phishguard.py`.
4. Access the user interface at `http://localhost:5000` in your web browser.

## Usage

1. Enter the URL you want to verify in the provided input field.
2. Click the "Verify" button to initiate the verification process.
3. Wait for the results to be displayed, indicating whether the URL is classified as phishing or not.
4. If the URL is identified as phishing, take appropriate action to avoid accessing it.

## Contributing

Contributions to PhishGuard are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
