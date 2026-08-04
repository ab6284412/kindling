# DMARC says WHO sent it, not WHAT it says
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: SenderLedger (publication)

## Summary
HN: "What DMARC protects you from, and what it does not." Within a domain that
passes DMARC, phishing still succeeds — DMARC authenticates the sender
(header.from alignment), it does not inspect message content.

## Lesson
SPF/DKIM/DMARC = sender authentication, not abuse prevention. Backend checklist
item: never treat "passed DMARC" as "trust this payload". Still validate
content, don't auto-click links or auto-parse attachments from mail, even when
all three checks pass.

## Drill

Goal: judge whether "passed DMARC" means anything in a given message.

Steps:
1. Send yourself an email (any provider), save the raw source / .eml.
2. Read the `Authentication-Results:` and `Received-SPF:` headers by hand.
3. Answer: did it pass SPF, DKIM, DMARC? For which domain? Is the envelope
   sender aligned with the header `From` (align = what DMARC checks)?
4. Now: what could still be phishing about this message even though every check
   passed? (Content, links, attachment names, lookalike display name.)

Self-check: you can explain what `p=`, `sp=`, `rua`, and "alignment" mean, and
state one thing DMARC cannot protect you from.

Why this matters: mail pipelines treat passing SPF/DKIM/DMARC as trust. It is
authentication, not permission to skip content validation.

## Further reading
- SenderLedger, https://senderledger.com/articles/what-dmarc-actually-protects-you-from — "What DMARC Actually Protects You From, and What It Does Not" (Aug 3 2026; on HN)
