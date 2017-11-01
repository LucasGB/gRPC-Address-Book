#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import time

import grpc

import agenda_pb2
import agenda_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Agenda(agenda_pb2_grpc.AgendaServicer):
  def __init__(self):
      self.contact_list = {}

  def add_contact(self, request, context):
      self.contact_list[request.name] = request.phone_number
      print self.contact_list
      return agenda_pb2.Reply(message="Contato adicionado a lista.")

  def delete_contact(self, request, context):
    self.contact_list.pop(request.name)
    print self.contact_list
    return agenda_pb2.Reply(message="Contato removido da lista.")

  def edit_contact(self, request, context):
    self.contact_list[request.name] = request.phone_number
    return agenda_pb2.Reply(message="Contato atualizado.")


  def list_contacts(self, request, context):
    for name, phone_number in self.contact_list.items():
      yield agenda_pb2.Contact(name=name, phone_number=phone_number)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  agenda_pb2_grpc.add_AgendaServicer_to_server(Agenda(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
