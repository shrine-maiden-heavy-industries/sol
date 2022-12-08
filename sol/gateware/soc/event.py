
# SPDX-License-Identifier: BSD-3-Clause
# This file is part of SOL.
#
# This file includes content Copyright (C) 2020 LambdaConcept.
# Per our BSD license, derivative files must include this license disclaimer.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

''' Peripheral interrupt helpers for SOL devices. '''


from lambdasoc.periph.event import IRQLine

from torii                  import Elaboratable, Module, Signal
from torii.lib.soc          import csr
from torii.util             import tracer

__all__ = (
	'EventSource',
	'IRQLine',
	'InterruptSource',
)


class EventSource:
	'''Event source.

	Parameters
	----------
	mode : ``'level'``, ``'rise'``, ``'fall'``
		Trigger mode. If ``'level'``, a notification is raised when the ``stb`` signal is high.
		If ``'rise'`` (or ``'fall'``) a notification is raised on a rising (or falling) edge
		of ``stb``.
	name : str
		Name of the event. If ``None`` (default) the name is inferred from the variable
		name this event source is assigned to.

	Attributes
	----------
	name : str
		Name of the event
	mode : ``'level'``, ``'rise'``, ``'fall'``
		Trigger mode.
	stb : Signal, in
		Event strobe.
	'''
	def __init__(self, *, mode = 'level', name = None, src_loc_at = 0):
		if name is not None and not isinstance(name, str):
			raise TypeError(f'Name must be a string, not {name!r}')

		choices = ('level', 'rise', 'fall')
		if mode not in choices:
			raise ValueError(f'Invalid trigger mode {mode!r}; must be one of {", ".join(choices)}')

		self.name = name or tracer.get_var_name(depth = 2 + src_loc_at)
		self.mode = mode
		self.stb  = Signal(name = f'{self.name}_stb')



class InterruptSource(Elaboratable):
	'''Interrupt source.

	A mean of gathering multiple event sources into a single interrupt request line.

	Parameters
	----------
	events : iter(:class:`EventSource`)
		Event sources.
	name : str
		Name of the interrupt source. If ``None`` (default) the name is inferred from the
		variable name this interrupt source is assigned to.

	Attributes
	----------
	name : str
		Name of the interrupt source.
	status : :class:`csr.Element`, read-only
		Event status register. Each bit displays the level of the strobe of an event source.
		Events are ordered by position in the `events` parameter.
	pending : :class:`csr.Element`, read/write
		Event pending register. If a bit is 1, the associated event source has a pending
		notification. Writing 1 to a bit clears it.
		Events are ordered by position in the `events` parameter.
	enable : :class:`csr.Element`, read/write
		Event enable register. Writing 1 to a bit enables its associated event source.
		Writing 0 disables it.
		Events are ordered by position in the `events` parameter.
	irq : :class:`IRQLine`, out
		Interrupt request. It is raised if any event source is enabled and has a pending
		notification.
	'''
	def __init__(self, events, *, name = None, src_loc_at = 0):
		if name is not None and not isinstance(name, str):
			raise TypeError(f'Name must be a string, not {name!r}')
		self.name = name or tracer.get_var_name(depth = 2 + src_loc_at)

		for event in events:
			if not isinstance(event, EventSource):
				raise TypeError(f'Event source must be an instance of EventSource, not {event!r}')
		self._events = list(events)

		width = len(events)
		self.status  = csr.Element(width, 'r',  name = f'{self.name}_status')
		self.pending = csr.Element(width, 'rw', name = f'{self.name}_pending')
		self.enable  = csr.Element(width, 'rw', name = f'{self.name}_enable')

		self.irq = IRQLine(name = f'{self.name}_irq')

	def elaborate(self, platform):
		m = Module()

		with m.If(self.pending.w_stb):
			m.d.sync += self.pending.r_data.eq(self.pending.r_data & ~self.pending.w_data)

		with m.If(self.enable.w_stb):
			m.d.sync += self.enable.r_data.eq(self.enable.w_data)

		for i, event in enumerate(self._events):
			m.d.sync += self.status.r_data[i].eq(event.stb)

			if event.mode in ('rise', 'fall'):
				event_stb_r = Signal.like(event.stb, name_suffix = '_r')
				m.d.sync += event_stb_r.eq(event.stb)

			event_trigger = Signal(name = f'{event.name}_trigger')
			if event.mode == 'level':
				m.d.comb += event_trigger.eq(event.stb)
			elif event.mode == 'rise':
				m.d.comb += event_trigger.eq(~event_stb_r & event.stb)
			elif event.mode == 'fall':
				m.d.comb += event_trigger.eq(event_stb_r & ~event.stb)
			else:
				raise ValueError(f'event.mode must be one of {{level, rise, fall}} not {event.mode!r}') # :nocov:

			with m.If(event_trigger):
				m.d.sync += self.pending.r_data[i].eq(1)

		m.d.comb += self.irq.eq((self.pending.r_data & self.enable.r_data).any())

		return m
