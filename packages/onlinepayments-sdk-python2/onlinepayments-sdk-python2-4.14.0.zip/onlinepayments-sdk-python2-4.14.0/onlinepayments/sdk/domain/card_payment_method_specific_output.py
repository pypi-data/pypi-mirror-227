# -*- coding: utf-8 -*-
#
# This class was auto-generated.
#
from onlinepayments.sdk.data_object import DataObject
from onlinepayments.sdk.domain.acquirer_information import AcquirerInformation
from onlinepayments.sdk.domain.card_essentials import CardEssentials
from onlinepayments.sdk.domain.card_fraud_results import CardFraudResults
from onlinepayments.sdk.domain.currency_conversion import CurrencyConversion
from onlinepayments.sdk.domain.external_token_linked import ExternalTokenLinked
from onlinepayments.sdk.domain.payment_product3208_specific_output import PaymentProduct3208SpecificOutput
from onlinepayments.sdk.domain.payment_product3209_specific_output import PaymentProduct3209SpecificOutput
from onlinepayments.sdk.domain.three_d_secure_results import ThreeDSecureResults


class CardPaymentMethodSpecificOutput(DataObject):
    """
    | Object containing the card payment method details
    """

    __acquirer_information = None
    __authenticated_amount = None
    __authorisation_code = None
    __card = None
    __currency_conversion = None
    __external_token_linked = None
    __fraud_results = None
    __initial_scheme_transaction_id = None
    __payment_option = None
    __payment_product3208_specific_output = None
    __payment_product3209_specific_output = None
    __payment_product_id = None
    __scheme_reference_data = None
    __three_d_secure_results = None
    __token = None

    @property
    def acquirer_information(self):
        """
        | Information about the acquirer used to process the transaction

        Type: :class:`onlinepayments.sdk.domain.acquirer_information.AcquirerInformation`
        """
        return self.__acquirer_information

    @acquirer_information.setter
    def acquirer_information(self, value):
        self.__acquirer_information = value

    @property
    def authenticated_amount(self):
        """
        | Allows amount to be authenticated to be different from amount authorized. (Amount in cents and always having 2 decimals)

        Type: long
        """
        return self.__authenticated_amount

    @authenticated_amount.setter
    def authenticated_amount(self, value):
        self.__authenticated_amount = value

    @property
    def authorisation_code(self):
        """
        | Card Authorization code as returned by the acquirer

        Type: str
        """
        return self.__authorisation_code

    @authorisation_code.setter
    def authorisation_code(self, value):
        self.__authorisation_code = value

    @property
    def card(self):
        """
        | Object containing card details

        Type: :class:`onlinepayments.sdk.domain.card_essentials.CardEssentials`
        """
        return self.__card

    @card.setter
    def card(self, value):
        self.__card = value

    @property
    def currency_conversion(self):
        """
        Type: :class:`onlinepayments.sdk.domain.currency_conversion.CurrencyConversion`
        """
        return self.__currency_conversion

    @currency_conversion.setter
    def currency_conversion(self, value):
        self.__currency_conversion = value

    @property
    def external_token_linked(self):
        """
        Type: :class:`onlinepayments.sdk.domain.external_token_linked.ExternalTokenLinked`
        """
        return self.__external_token_linked

    @external_token_linked.setter
    def external_token_linked(self, value):
        self.__external_token_linked = value

    @property
    def fraud_results(self):
        """
        | Fraud results contained in the CardFraudResults object

        Type: :class:`onlinepayments.sdk.domain.card_fraud_results.CardFraudResults`
        """
        return self.__fraud_results

    @fraud_results.setter
    def fraud_results(self, value):
        self.__fraud_results = value

    @property
    def initial_scheme_transaction_id(self):
        """
        | The unique scheme transactionId of the initial transaction that was performed with SCA. In case this is unknown a scheme transactionId of an earlier transaction part of the same sequence can be used as a fall-back. Strongly advised to be submitted for any MerchantInitiated or recurring transaction (a subsequent one).

        Type: str
        """
        return self.__initial_scheme_transaction_id

    @initial_scheme_transaction_id.setter
    def initial_scheme_transaction_id(self, value):
        self.__initial_scheme_transaction_id = value

    @property
    def payment_option(self):
        """
        | The specific payment option for the payment. To be used as a complement of the more generic paymentProductId (oney, banquecasino, cofidis), which allows to define a variation of the selected paymentProductId (ex: facilypay3x, banquecasino4x, cofidis3x-sansfrais, ...). List of modalities included in the payment product page.

        Type: str
        """
        return self.__payment_option

    @payment_option.setter
    def payment_option(self, value):
        self.__payment_option = value

    @property
    def payment_product3208_specific_output(self):
        """
        | OneyDuplo Leroy Merlin specific details

        Type: :class:`onlinepayments.sdk.domain.payment_product3208_specific_output.PaymentProduct3208SpecificOutput`
        """
        return self.__payment_product3208_specific_output

    @payment_product3208_specific_output.setter
    def payment_product3208_specific_output(self, value):
        self.__payment_product3208_specific_output = value

    @property
    def payment_product3209_specific_output(self):
        """
        | OneyDuplo Alcampo specific details

        Type: :class:`onlinepayments.sdk.domain.payment_product3209_specific_output.PaymentProduct3209SpecificOutput`
        """
        return self.__payment_product3209_specific_output

    @payment_product3209_specific_output.setter
    def payment_product3209_specific_output(self, value):
        self.__payment_product3209_specific_output = value

    @property
    def payment_product_id(self):
        """
        | Payment product identifier - Please see Products documentation for a full overview of possible values.

        Type: int
        """
        return self.__payment_product_id

    @payment_product_id.setter
    def payment_product_id(self, value):
        self.__payment_product_id = value

    @property
    def scheme_reference_data(self):
        """
        | This is the unique Scheme Reference Data from the initial transaction that was performed with a Strong Customer Authentication. In case this value is unknown, a Scheme Reference of an earlier transaction that was part of the same sequence can be used as a fall-back. Still, it is strongly advised to submit this value for any Merchant Initiated Transaction or any recurring transaction (hereby defined as "Subsequent").

        Type: str
        """
        return self.__scheme_reference_data

    @scheme_reference_data.setter
    def scheme_reference_data(self, value):
        self.__scheme_reference_data = value

    @property
    def three_d_secure_results(self):
        """
        | 3D Secure results object

        Type: :class:`onlinepayments.sdk.domain.three_d_secure_results.ThreeDSecureResults`
        """
        return self.__three_d_secure_results

    @three_d_secure_results.setter
    def three_d_secure_results(self, value):
        self.__three_d_secure_results = value

    @property
    def token(self):
        """
        | ID of the token. This property is populated when the payment was done with a token or when the payment was tokenized.

        Type: str
        """
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value

    def to_dictionary(self):
        dictionary = super(CardPaymentMethodSpecificOutput, self).to_dictionary()
        if self.acquirer_information is not None:
            dictionary['acquirerInformation'] = self.acquirer_information.to_dictionary()
        if self.authenticated_amount is not None:
            dictionary['authenticatedAmount'] = self.authenticated_amount
        if self.authorisation_code is not None:
            dictionary['authorisationCode'] = self.authorisation_code
        if self.card is not None:
            dictionary['card'] = self.card.to_dictionary()
        if self.currency_conversion is not None:
            dictionary['currencyConversion'] = self.currency_conversion.to_dictionary()
        if self.external_token_linked is not None:
            dictionary['externalTokenLinked'] = self.external_token_linked.to_dictionary()
        if self.fraud_results is not None:
            dictionary['fraudResults'] = self.fraud_results.to_dictionary()
        if self.initial_scheme_transaction_id is not None:
            dictionary['initialSchemeTransactionId'] = self.initial_scheme_transaction_id
        if self.payment_option is not None:
            dictionary['paymentOption'] = self.payment_option
        if self.payment_product3208_specific_output is not None:
            dictionary['paymentProduct3208SpecificOutput'] = self.payment_product3208_specific_output.to_dictionary()
        if self.payment_product3209_specific_output is not None:
            dictionary['paymentProduct3209SpecificOutput'] = self.payment_product3209_specific_output.to_dictionary()
        if self.payment_product_id is not None:
            dictionary['paymentProductId'] = self.payment_product_id
        if self.scheme_reference_data is not None:
            dictionary['schemeReferenceData'] = self.scheme_reference_data
        if self.three_d_secure_results is not None:
            dictionary['threeDSecureResults'] = self.three_d_secure_results.to_dictionary()
        if self.token is not None:
            dictionary['token'] = self.token
        return dictionary

    def from_dictionary(self, dictionary):
        super(CardPaymentMethodSpecificOutput, self).from_dictionary(dictionary)
        if 'acquirerInformation' in dictionary:
            if not isinstance(dictionary['acquirerInformation'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['acquirerInformation']))
            value = AcquirerInformation()
            self.acquirer_information = value.from_dictionary(dictionary['acquirerInformation'])
        if 'authenticatedAmount' in dictionary:
            self.authenticated_amount = dictionary['authenticatedAmount']
        if 'authorisationCode' in dictionary:
            self.authorisation_code = dictionary['authorisationCode']
        if 'card' in dictionary:
            if not isinstance(dictionary['card'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['card']))
            value = CardEssentials()
            self.card = value.from_dictionary(dictionary['card'])
        if 'currencyConversion' in dictionary:
            if not isinstance(dictionary['currencyConversion'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['currencyConversion']))
            value = CurrencyConversion()
            self.currency_conversion = value.from_dictionary(dictionary['currencyConversion'])
        if 'externalTokenLinked' in dictionary:
            if not isinstance(dictionary['externalTokenLinked'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['externalTokenLinked']))
            value = ExternalTokenLinked()
            self.external_token_linked = value.from_dictionary(dictionary['externalTokenLinked'])
        if 'fraudResults' in dictionary:
            if not isinstance(dictionary['fraudResults'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['fraudResults']))
            value = CardFraudResults()
            self.fraud_results = value.from_dictionary(dictionary['fraudResults'])
        if 'initialSchemeTransactionId' in dictionary:
            self.initial_scheme_transaction_id = dictionary['initialSchemeTransactionId']
        if 'paymentOption' in dictionary:
            self.payment_option = dictionary['paymentOption']
        if 'paymentProduct3208SpecificOutput' in dictionary:
            if not isinstance(dictionary['paymentProduct3208SpecificOutput'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['paymentProduct3208SpecificOutput']))
            value = PaymentProduct3208SpecificOutput()
            self.payment_product3208_specific_output = value.from_dictionary(dictionary['paymentProduct3208SpecificOutput'])
        if 'paymentProduct3209SpecificOutput' in dictionary:
            if not isinstance(dictionary['paymentProduct3209SpecificOutput'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['paymentProduct3209SpecificOutput']))
            value = PaymentProduct3209SpecificOutput()
            self.payment_product3209_specific_output = value.from_dictionary(dictionary['paymentProduct3209SpecificOutput'])
        if 'paymentProductId' in dictionary:
            self.payment_product_id = dictionary['paymentProductId']
        if 'schemeReferenceData' in dictionary:
            self.scheme_reference_data = dictionary['schemeReferenceData']
        if 'threeDSecureResults' in dictionary:
            if not isinstance(dictionary['threeDSecureResults'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['threeDSecureResults']))
            value = ThreeDSecureResults()
            self.three_d_secure_results = value.from_dictionary(dictionary['threeDSecureResults'])
        if 'token' in dictionary:
            self.token = dictionary['token']
        return self
