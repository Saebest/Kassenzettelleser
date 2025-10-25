package leser

import "mime/multipart"

type KassenzettelLeser interface {
	ReadKassenzettel(image multipart.File) (string, error)
}
