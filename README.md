# enumerate\_certificates\_issued\_by\_CA

## Description
This tool takes in a list of ca id's from crt.sh, and outputs a list of domains it can find from those CA ID's.

I made it to show how some AWS resources can be enumerated using certificate transparency logs and viewing certificates issued by the Amazon root CAs.

## Example CAIDs

They can be found in this [file](example_aws_caids.txt)

These were found in crt.sh. They can be found by searching for the CA on crt.sh and looking in the URL. These CAIDs are from the Amazon root CAs.
