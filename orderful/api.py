# pylint: disable=line-too-long
from urllib.parse import urlencode

import requests


class OrderfulAPI:
    """Initalization of Orderful API"""
    def __init__(self, stream, orderful_api_key):
        self.stream = stream
        self.orderful_api_key = orderful_api_key
        self.api_headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "orderful-api-key": self.orderful_api_key,
        }
        self.client = requests.Session()
        self.client.headers.update(self.api_headers)

    def get_base_url(self):
        """get base url for orderful api

        Returns:
            string: https base url for orderful api
        """
        return "https://api.orderful.com/v3"

    def is_enabled(self):
        """Check to see if the orderful api is enabled"""
        return self.stream and self.orderful_api_key

    def is_live_stream(self):
        """Check to see if the stream is live"""
        return self.stream == "LIVE"

    def get_transactions_from_poller_bucket(
        self,
        bucket_id,
        limit=False
    ):
        """_summary_

        Args:
            bucket_id (int): Orderful Polling Bucket ID
            limit (int, optional): limit the number of transactions. Defaults to 30 when False.

        Returns:
            List: List of transactions from the polling bucket
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/polling-buckets/{bucket_id}"
        params = {}
        if limit:
            params.update(limit=limit)

        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def list_relationships(
        self,
        bucket_id,
        auto_send=False,
        limit=False,
        prev_cursor=False,
        next_cursor=False
    ):
        """List Relationships

        Args:
            bucket_id (int): Orderful Polling Bucket ID
            auto_send (bool, optional): Filter by the relationship
                auto-send configuration.
                Defaults to False.
            limit (int, optional): The number of items to return in the
                result set. Defaults to False.
            prev_cursor (str, optional): Used in subsequent calls for
                paginated data. Defaults to False.
            next_cursor (str, optional): Used in subsequent calls for
                paginated data. Defaults to False.

        Returns:
            List: List of relationships
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/relationships/{bucket_id}"
        params = {}
        if auto_send:
            params.update(auto_send=auto_send)
        if limit:
            params.update(limit=limit)
        if prev_cursor:
            params.update(prev_cursor=prev_cursor)
        if next_cursor:
            params.update(next_cursor=next_cursor)

        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_organization_details(self):
        """Get Orderful Organization Details

        Returns:
            JSON:  object representing orderful organization details
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/organizations/me"

        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

    def convert_data(
        self,
        origin_content,
        destination_content
    ):
        """Conver orderful data from one format to another

        Args:
            origin_content (string): Origin content format
            destination_content (string): Destination content format

        Raises:
            UserError: when the request to convert data fails

        Returns:
            JSON: JSON object response for data conversion
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/convert"
        headers = {
            "Content-Type": origin_content,
            "Accept": destination_content
        }
        response = self.client.post(
            url,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    def create_transaction(
        self,
        orderful_type,
        message,
        sender_isa_id,
        receiver_isa_id
    ):
        """Create Orderful Transaction

        Args:
            orderful_type (string): transaction type
            message (json): message or document details for transaction
            senderIsaId (string): ISA ID of sender
            receiverIsaId (string): ISA ID of receiver

        Raises:
            UserError: when the request to create a new transaction fails

        Returns:
            string: ID of newly created transaction
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/transactions"
        payload = {
            "type": {"name": orderful_type},
            "stream": self.stream,
            "message": message,
            "sender": {"isaId": sender_isa_id},
            "receiver": {"isaId": receiver_isa_id},
        }
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["id"]

    def list_transactions(
        self,
        prev_cursor=False,
        next_cursor=False,
        created_at=False,
        business_numbers=False,
        transaction_type=False,
        validation_status=False,
        delivery_status=False,
        acknowledgment_status=False,
        sender_isa_id=False,
        receiver_isa_id=False,
        reference_identifier=False,
        sender_interchange_reference_identifier=False,
        sender_group_reference_identifier=False,
        sender_transaction_reference_identifier=False,
        receiver_interchange_reference_identifier=False,
        receiver_group_reference_identifier=False,
        receiver_transaction_reference_identifier=False
    ):
        """List Transactions

        Args:
            createdAt (date, optional): The date and time that the Transactions were created on or before, in ISO-8601 format.
            businessNumbers (Array(string), optional): Indicates which business number(s) you would like to list Transactions from.
                You may indicate up to 5 business numbers.
            transactionType (Array(string), optional): Indicates the Transaction Type(s) you would like to filter by.
                You may indicate up to 5 Transaction Types.
            validationStatus (Array(string), optional): The one or more validation status(es) you would like to filter by.
            deliveryStatus (Array(string), optional): The one or more delivery status(es) you would like to filter by.
            acknowledgmentStatus (Array(string), optional): The one or more acknowledgment status(es) you would like to filter by.
            senderIsaId (Array(string), optional): The Sender ISA ID(s) that you would like to list Transactions from.
                You may indicate up to 5 Sender ISA IDs.
            receiverIsaId (Array(string), optional): The Receiver ISA ID(s) that you would like to list Transactions from.
                You may indicate up to 5 Receiver ISA IDs.
            referenceIdentifier (string, optional): Reference Identifier Value you would like to filter by.
            senderInterchangeReferenceIdentifier (string, optional): Sender's Interchange Reference Identifier Value you would like to filter by.
            senderGroupReferenceIdentifier (string, optional): Sender's (Functional) Group Reference Identifier Value you would like to filter by.
            senderTransactionReferenceIdentifier (string, optional): Sender's Transaction Reference Identifier Value you would like to filter by.
            receiverInterchangeReferenceIdentifier (string, optional): Receiver's Interchange Reference Identifier Value you would like to filter by.
            receiverGroupReferenceIdentifier (string, optional): Receiver's (Functional) Group Reference Identifier Value you would like to filter by.
            receiverTransactionReferenceIdentifier (string, optional): Receiver's Transaction Reference Identifier Value you would like to filter by.

        Raises:
            UserError: when the request to get transactions fails

        Returns:
            JSON: List of orderful transactions
        """
        params = {}
        if prev_cursor:
            params.update(prevCursor=prev_cursor)
        if next_cursor:
            params.update(nextCursor=next_cursor)
        if created_at:
            params.update(createdAt=created_at)
        if business_numbers:
            params.update(businessNumbers=business_numbers)
        if transaction_type:
            params.update(transactionType=transaction_type)
        if validation_status:
            params.update(validationStatus=validation_status)
        if delivery_status:
            params.update(deliveryStatus=delivery_status)
        if acknowledgment_status:
            params.update(acknowledgmentStatus=acknowledgment_status)
        if sender_isa_id:
            params.update(senderIsaId=sender_isa_id)
        if receiver_isa_id:
            params.update(receiverIsaId=receiver_isa_id)
        if reference_identifier:
            params.update(referenceIdentifier=reference_identifier)
        if sender_interchange_reference_identifier:
            params.update(senderInterchangeReferenceIdentifier=sender_interchange_reference_identifier)
        if sender_group_reference_identifier:
            params.update(senderGroupReferenceIdentifier=sender_group_reference_identifier)
        if sender_transaction_reference_identifier:
            params.update(senderTransactionReferenceIdentifier=sender_transaction_reference_identifier)
        if receiver_interchange_reference_identifier:
            params.update(receiverInterchangeReferenceIdentifier=receiver_interchange_reference_identifier)
        if receiver_group_reference_identifier:
            params.update(receiverGroupReferenceIdentifier=receiver_group_reference_identifier)
        if receiver_transaction_reference_identifier:
            params.update(receiverTransactionReferenceIdentifier=receiver_transaction_reference_identifier)

        baseurl = self.get_base_url()
        url = f"{baseurl}/transactions"

        response = self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        metadata = data["metadata"]
        transactions = data["data"]
        return metadata, transactions

    def get_transaction(self, transaction_id, include_message=False):
        """Get Orderful Transaction

        Args:
            transactionId (string): ID of the transaction
            include_message (bool, optional): whether to include message content in response. Defaults to False.

        Raises:
            UserError: when the request to get transaction fails

        Returns:
            JSON: object representing  orderful transaction
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/transactions/{transaction_id}"
        params = {}
        if include_message:
            params.update(expand="message")

        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_transaction_message(self, transaction_id):
        """Get Orderful Transaction Message

        Args:
            transactionId (string): ID of the transaction

        Raises:
            UserError: when the request to get transaction message fails

        Returns:
            JSON: Data that represents a transaction message
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/transactions/{transaction_id}/message"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

    def create_acknowledgment(self, transaction_id, status, errors=False):
        """Create Orderful Acknowledgment

        Args:
            transaction_id (string): ID of the transaction
            status (string): status of the acknowledgment
            errors (Array, optional): list of errors. Defaults to False.

        Raises:
            UserError: when the request to create acknowledgment fails

        Returns:
            string: ID of newly created acknowledgment
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/transactions/{transaction_id}/acknowledgments"
        payload = {
            "status": status
        }
        if errors:
            payload.update(errors=errors)
        response = self.client.post(url, json=payload)
        response.raise_for_status()

    def get_acknowledgment(self, transaction_id):
        """Get Orderful Acknowledgment

        Args:
            transactionId (string): ID of the transaction

        Returns:
            JSON: object representing an orderful acknowledgment
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/transactions/{transaction_id}/acknowledgment"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

    def get_attachment(self, attachment_id):
        """Get attachment

        Args:
            attachmentId (string): ID of the attachment

        Raises:
            UserError: when the request to get attachment fails

        Returns:
            JSON: object that represents an orderful attachment
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/attachments/{attachment_id}"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

    def get_attachment_content(self, attachment_id):
        """Get Orderful Attachment Content

        Args:
            attachmentId (string): ID of the attachment

        Raises:
            UserError: when the request to get attachment content fails

        Returns:
            string: content of the attachment
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/attachments/{attachment_id}/content"
        response = self.client.get(url)
        response.raise_for_status()
        return response.content

    def approve_delivery(self, delivery_id, note=False):
        """Approve Orderful Delivery

        Args:
            delivery_id (string): ID of the delivery
            note (string, optional): note for the approval. Defaults to False.

        Raises:
            UserError: when the request to approve delivery fails
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/deliveries/{delivery_id}/approve"
        payload = {}
        if note:
            payload.update(note=note)
        response = self.client.post(url, json=payload)
        response.raise_for_status()

    def fail_delivery(self, delivery_id, note=False):
        """Fail Orderful Delivery

        Args:
            delivery_id (string): ID of the delivery
            note (string, optional): note for the failure. Defaults to False.

        Raises:
            UserError: when the request to fail delivery fails
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/deliveries/{delivery_id}/fail"
        payload = {}
        if note:
            payload.update(note=note)
        response = self.client.post(url, json=payload)
        response.raise_for_status()

    def get_delivery(self, delivery_id):
        """Get Orderful Delivery

        Args:
            delivery_id (string): ID of the delivery

        Raises:
            UserError: when the request to get delivery fails

        Returns:
            JSON: object representing an orderful delivery
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/deliveries/{delivery_id}"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

    def generate_label(
        self,
        label_type,
        **kwargs
    ):
        """Generate Orderful Label

        Args:
            label_type (string): type of label to generate
            kwargs (dict): additional parameters

        Raises:
            UserError: when the request to generate label fails

        Returns:
            JSON: object representing an orderful label
        """
        baseurl = self.get_base_url()
        url = f"{baseurl}/labels/{label_type}"
        response = self.client.post(url, json=kwargs)
        response.raise_for_status()
        return response.json()
