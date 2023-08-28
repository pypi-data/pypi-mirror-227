from abc import ABC
from typing import List, Tuple, Optional, Collection, Iterable

PUT_RECORD_COLLECTION = Collection[Tuple[bytes, int, Optional[bytes]]]


class Backend(ABC):
    def validate_payloads(self, payloads: Iterable[bytes]):
        if self.max_payload_size is None:
            return
        for payload in payloads:
            if len(payload) > self.max_payload_size:
                raise ValueError(
                    f"payload exceeds PAYLOAD_MAX_SIZE ({len(payload)} > {self.max_payload_size})"
                )

    def validate_hashes(self, hashes: Iterable[Optional[bytes]]) -> None:
        for hsh in hashes:
            if hsh is not None and len(hsh) != self.hash_size:
                raise ValueError(
                    f"hash size is not HASH_SIZE ({len(hsh)} != {self.hash_size})"
                )

    def filter_by_rate_limit(
        self, data: PUT_RECORD_COLLECTION, rate_limit_seconds: Optional[int] = None
    ) -> PUT_RECORD_COLLECTION:
        if rate_limit_seconds is None:
            return data

        allowed = set(
            self.rate_limit(
                [x[2] for x in data if x[2] is not None],
                interval_seconds=rate_limit_seconds,
            )
        )
        return [x for x in data if x[2] is None or x[2] in allowed]

    @property
    def max_payload_size(self) -> Optional[int]:
        raise NotImplementedError

    @property
    def hash_size(self) -> int:
        raise NotImplementedError

    def create(self) -> None:
        raise NotImplementedError

    def destroy(self) -> None:
        raise NotImplementedError

    def batch_put(
        self,
        data: PUT_RECORD_COLLECTION,
        priority: int,
        delay: int,
        failure_base_delay: int,
        rate_limit_seconds: Optional[int] = None,
    ) -> int:
        raise NotImplementedError

    def ack(self, task_id: int) -> None:
        raise NotImplementedError

    def batch_get(
        self, topic: int, size: int, visibility_timeout: int
    ) -> List["Message"]:
        raise NotImplementedError

    def batch_soft_nack(self, task_ids: Collection[int]) -> None:
        raise NotImplementedError

    def batch_nack(self, task_ids: Collection[int]) -> None:
        raise NotImplementedError

    def batch_touch(self, task_ids: Collection[int], visibility_timeout: int) -> None:
        raise NotImplementedError

    def list_topics(self) -> List[Tuple[int, int]]:
        raise NotImplementedError

    def get_topic_size(self, topic: int) -> int:
        raise NotImplementedError

    def acquire_topic(
        self, topic_lock_visibility_timeout: int
    ) -> Optional["TopicLock"]:
        raise NotImplementedError

    def batch_release_topic(self, topics: Collection[int]) -> None:
        raise NotImplementedError

    def batch_touch_topic(
        self, topics: Collection[int], topic_lock_visibility_timeout: int
    ) -> None:
        raise NotImplementedError

    def rate_limit(self, hshes: Iterable[bytes], interval_seconds: int) -> List[bytes]:
        raise NotImplementedError

    def override_rate_limit(
        self, hshes: Collection[bytes], interval_seconds: int
    ) -> None:
        raise NotImplementedError


class TopicLock:
    def __init__(self, idx: int, backend: Backend, visibility_timeout: int):
        self.idx = idx
        self.backend = backend
        self.visibility_timeout = visibility_timeout
        self.released = False

    def __str__(self):
        return f"TopicLock({self.idx})"

    def release(self):
        if self.released:
            raise RuntimeError("Lock has already been released")
        self.backend.batch_release_topic([self.idx])
        self.released = True

    def touch(self):
        if self.released:
            raise RuntimeError("Lock has already been released")
        self.backend.batch_touch_topic([self.idx], self.visibility_timeout)


class Message:
    FIELDS = ["payload", "idx", "backend", "visibility_timeout", "status"]

    def __init__(
        self,
        payload: bytes,
        idx: int,
        backend: Backend,
        visibility_timeout: int,
        status: Optional[bool] = None,
    ):
        self.payload = payload
        self.idx = idx
        self.backend = backend
        self.visibility_timeout = visibility_timeout
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.status is None:
            self.nack()

    @property
    def released(self):
        return self.status is not None

    def ack(self):
        if self.released:
            raise RuntimeError("Message has already been relinquished")
        self.status = True
        self.backend.ack(self.idx)

    def nack(self):
        if self.released:
            raise RuntimeError("Message has already been relinquished")
        self.status = False
        self.backend.batch_nack([self.idx])

    def soft_nack(self):
        if self.released:
            raise RuntimeError("Message has already been relinquished")
        self.status = False
        self.backend.batch_soft_nack([self.idx])

    def touch(self):
        if self.released:
            raise RuntimeError("Message has already been relinquished")
        self.backend.batch_touch([self.idx], visibility_timeout=self.visibility_timeout)

    def check(self) -> bool:
        """
        Check whether the message is still owned by this consumer.
        Use a local estimate based on when the message was acquired.
        """
        if self.released:
            return False

        raise NotImplementedError
